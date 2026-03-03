import fs from "node:fs";
import path from "node:path";
import yaml from "js-yaml";
import {
  buildSchema,
  getIntrospectionQuery,
  graphqlSync,
} from "graphql";

const ROOT = process.cwd();
const DATA_ROOT = path.join(
  ROOT,
  "kitty-specs",
  "001-wai-standards-yaml-ld-ingestion",
  "research",
);
const OUT_ROOT = path.join(ROOT, "dist", "api", "v1");

const SCHEMA_TEXT = `schema {
  query: Query
}

type Query {
  successCriterion(id: String!): SuccessCriterion
  allSuccessCriteria: [SuccessCriterion!]!
  guideline(id: String!): Guideline
  allGuidelines: [Guideline!]!
  technique(id: String!): Technique
  allTechniques: [Technique!]!
  failure(id: String!): Failure
  allFailures: [Failure!]!
}

enum ComplianceLevel {
  A
  AA
  AAA
}

type Guideline {
  id: ID!
  ref_id: String!
  title: String!
  version: String!
  standard_id: String!
  url: String
}

type Technique {
  id: ID!
  title: String!
  url: String!
  source: String!
  status: String
  relatedSC: [String!]!
}

type Failure {
  id: ID!
  title: String!
  url: String!
  source: String!
  status: String
  relatedSC: [String!]!
}

type SuccessCriterion {
  id: ID!
  ref_id: String!
  title: String!
  description: String!
  level: ComplianceLevel!
  version: String!
  url: String!
  parentGuideline: Guideline!
  sufficientTechniques: [Technique!]
  advisoryTechniques: [Technique!]
  failures: [Failure!]
  tags: [String!]
  isNewIn22: Boolean!
  hasLegacyVersion: Boolean!
  supersededBy: String
  supersedes: String
}
`;

function ensureDir(directoryPath) {
  fs.mkdirSync(directoryPath, { recursive: true });
}

function writeJson(filePath, payload) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, JSON.stringify(payload, null, 2) + "\n", "utf8");
}

function writeText(filePath, content) {
  ensureDir(path.dirname(filePath));
  fs.writeFileSync(filePath, content, "utf8");
}

function slugifyRef(value) {
  return String(value || "")
    .trim()
    .replace(/\./g, "-")
    .replace(/[^a-zA-Z0-9\-_]/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
    .toLowerCase();
}

function walkFiles(rootDir) {
  const output = [];
  const stack = [rootDir];
  const ignoredDirs = new Set([".git", "node_modules", "dist"]);
  while (stack.length) {
    const current = stack.pop();
    const entries = fs.readdirSync(current, { withFileTypes: true });
    for (const entry of entries) {
      const nextPath = path.join(current, entry.name);
      if (entry.isDirectory()) {
        if (ignoredDirs.has(entry.name)) {
          continue;
        }
        stack.push(nextPath);
        continue;
      }
      if (entry.name.endsWith(".yaml") || entry.name.endsWith(".yml")) {
        output.push(nextPath);
      }
    }
  }
  return output.sort();
}

function loadYaml(filePath) {
  const raw = fs.readFileSync(filePath, "utf8");
  const parsed = yaml.load(raw);
  if (typeof parsed !== "object" || parsed === null) {
    return null;
  }
  return parsed;
}

function toCanonicalId(raw, fallbackPrefix) {
  if (!raw) {
    return fallbackPrefix;
  }
  const value = String(raw).trim();
  if (value.startsWith("http://") || value.startsWith("https://") || value.startsWith("urn:")) {
    return value;
  }
  return `urn:wai:${value}`;
}

function normalizeLevel(level) {
  const normalized = String(level || "A").toUpperCase();
  if (normalized === "A" || normalized === "AA" || normalized === "AAA") {
    return normalized;
  }
  return "A";
}

function findGuidelineRef(scCode) {
  const parts = String(scCode || "").split(".");
  if (parts.length >= 2) {
    return `${parts[0]}.${parts[1]}`;
  }
  return "unknown";
}

function extractVersion(standardId) {
  const match = String(standardId || "").match(/(\d+\.\d+)/);
  return match ? match[1] : "unknown";
}

function deepCollectLinkedData(node, state, sourcePath, pointer = "$") {
  if (Array.isArray(node)) {
    node.forEach((value, index) => deepCollectLinkedData(value, state, sourcePath, `${pointer}[${index}]`));
    return;
  }
  if (typeof node !== "object" || node === null) {
    return;
  }

  const idCandidate = node["@id"] || node.id || node.standard_id || node.graph_id || null;
  const typeCandidate = node["@type"] || node.type || node.kind || null;

  if (idCandidate) {
    const id = toCanonicalId(idCandidate, "urn:wai:node");
    const type = typeCandidate ? String(typeCandidate) : "Thing";
    if (!state.nodesById.has(id)) {
      state.nodesById.set(id, {
        id,
        type,
        source_file: sourcePath,
        source_pointer: pointer,
        raw_id: idCandidate,
        raw_type: typeCandidate || "",
      });
    }
  }

  for (const [key, value] of Object.entries(node)) {
    if (key === "@id" || key === "@type") {
      continue;
    }
    if (typeof value === "string") {
      if (key.endsWith("_id") || key === "id" || key === "from" || key === "to") {
        const fromId = idCandidate ? toCanonicalId(idCandidate, "urn:wai:node") : null;
        const toId = toCanonicalId(value, "urn:wai:ref");
        if (fromId && toId && fromId !== toId) {
          state.edges.push({
            from: fromId,
            to: toId,
            relation: key,
            source_file: sourcePath,
            source_pointer: pointer,
          });
        }
      }
    }
  }

  for (const [key, value] of Object.entries(node)) {
    deepCollectLinkedData(value, state, sourcePath, `${pointer}.${key}`);
  }
}

function extractScFromNormative(filePath, document, state) {
  const criteria = Array.isArray(document.normative_success_criteria)
    ? document.normative_success_criteria
    : [];
  if (!criteria.length) {
    return;
  }

  const standardId = String(document.standard_id || "unknown");
  if (!standardId.startsWith("wcag-")) {
    return;
  }
  const version = extractVersion(standardId);
  const wcag22 = version === "2.2";

  for (const criterion of criteria) {
    const refId = String(criterion.code || "").trim();
    if (!refId) {
      continue;
    }
    const guidelineRef = findGuidelineRef(refId);
    const guidelineKey = `${standardId}:${guidelineRef}`;

    if (!state.guidelines.has(guidelineKey)) {
      state.guidelines.set(guidelineKey, {
        id: `urn:wai:guideline:${standardId}:${guidelineRef}`,
        ref_id: guidelineRef,
        title: `Guideline ${guidelineRef}`,
        version,
        standard_id: standardId,
        url: document.tr_url || "",
      });
    }

    const scId =
      criterion["@id"] ||
      criterion.url ||
      `urn:wai:success-criterion:${standardId}:${refId}`;

    state.scRecords.push({
      id: toCanonicalId(scId, "urn:wai:success-criterion"),
      ref_id: refId,
      title: String(criterion.title || "").trim(),
      description: String(criterion.normative_text || "").trim(),
      level: normalizeLevel(criterion.level),
      version,
      url: String(criterion.url || document.tr_url || "").trim(),
      parentGuideline: state.guidelines.get(guidelineKey),
      sufficientTechniques: [],
      advisoryTechniques: [],
      failures: [],
      tags: [],
      isNewIn22: wcag22,
      hasLegacyVersion: false,
      supersededBy: null,
      supersedes: null,
      standard_id: standardId,
      source_file: filePath,
    });
  }
}

function extractWcagRefs(text) {
  const refs = new Set();
  const raw = String(text || "");
  const compactMatches = raw.match(/wcag\s*([0-9]{3,4})/gi) || [];
  for (const token of compactMatches) {
    const digits = token.replace(/[^0-9]/g, "");
    if (digits.length === 3) {
      refs.add(`${digits[0]}.${digits[1]}.${digits[2]}`);
    }
    if (digits.length === 4) {
      refs.add(`${digits[0]}.${digits[1]}.${digits.slice(2)}`);
    }
  }
  const dottedMatches = raw.match(/\b([1-4]\.[0-9]{1,2}\.[0-9]{1,2})\b/g) || [];
  for (const token of dottedMatches) {
    refs.add(token);
  }
  return [...refs];
}

function extractTechniquesAndFailures(ruleCatalogPath, state) {
  if (!fs.existsSync(ruleCatalogPath)) {
    return;
  }
  const catalog = loadYaml(ruleCatalogPath);
  if (!catalog || !Array.isArray(catalog.rule_sets)) {
    return;
  }

  for (const set of catalog.rule_sets) {
    const setId = String(set.id || "unknown");
    const setTitle = String(set.title || setId);
    const rules = Array.isArray(set.rules) ? set.rules : [];

    for (const rule of rules) {
      const title = String(rule.title || rule.id || "").trim();
      if (!title) {
        continue;
      }
      const refs = extractWcagRefs(title);
      if (!refs.length) {
        continue;
      }
      const baseRecord = {
        id: `urn:wai:${setId}:${rule.id}`,
        title,
        url: String(rule.url || set.catalog_url || "").trim(),
        source: setTitle,
        status: String(rule.status || "").trim(),
        relatedSC: refs,
      };

      const isFailure = /\bfailure\b/i.test(title);
      const isActRuleSet = setId.includes("w3c-act");

      if (isFailure) {
        state.failures.push(baseRecord);
      } else {
        if (isActRuleSet) {
          state.sufficientTechniques.push(baseRecord);
        } else {
          state.advisoryTechniques.push(baseRecord);
        }
      }
    }
  }
}

function buildIntrospection(schemaText) {
  const schema = buildSchema(schemaText);
  const query = getIntrospectionQuery();
  const result = graphqlSync({
    schema,
    source: query,
  });
  if (result.errors?.length) {
    throw new Error(`Failed introspection generation: ${result.errors[0].message}`);
  }
  return result;
}

function indexByRef(records) {
  const map = new Map();
  for (const record of records) {
    if (!record.ref_id) {
      continue;
    }
    if (!map.has(record.ref_id)) {
      map.set(record.ref_id, []);
    }
    map.get(record.ref_id).push(record);
  }
  return map;
}

function enrichVersionLinks(state) {
  const byRef = indexByRef(state.scRecords);
  for (const [refId, records] of byRef.entries()) {
    const wcag20 = records.find((record) => record.version === "2.0");
    const wcag22 = records.find((record) => record.version === "2.2");
    if (wcag20 && wcag22) {
      wcag22.hasLegacyVersion = true;
      wcag22.supersedes = wcag20.id;
      wcag20.supersededBy = wcag22.id;
    }
    if (records.length > 1 && !wcag20 && !wcag22) {
      records.forEach((record, index) => {
        if (index < records.length - 1) {
          record.supersededBy = records[index + 1].id;
        }
      });
    }
    byRef.set(refId, records);
  }
}

function joinScRelationships(state) {
  const byRef = indexByRef(state.scRecords);

  const attach = (collection, targetField) => {
    for (const item of collection) {
      for (const ref of item.relatedSC || []) {
        const records = byRef.get(ref) || [];
        for (const record of records) {
          record[targetField].push(item);
        }
      }
    }
  };

  attach(state.sufficientTechniques, "sufficientTechniques");
  attach(state.advisoryTechniques, "advisoryTechniques");
  attach(state.failures, "failures");
}

function writeEndpoints(state) {
  ensureDir(OUT_ROOT);

  const scSorted = [...state.scRecords].sort((a, b) => a.ref_id.localeCompare(b.ref_id));
  const guidelineSorted = [...state.guidelines.values()].sort((a, b) => a.ref_id.localeCompare(b.ref_id));
  const techniqueSorted = [...state.sufficientTechniques, ...state.advisoryTechniques].sort((a, b) =>
    a.id.localeCompare(b.id),
  );
  const failureSorted = [...state.failures].sort((a, b) => a.id.localeCompare(b.id));

  writeJson(path.join(OUT_ROOT, "sc", "all.json"), scSorted);
  writeJson(path.join(OUT_ROOT, "success-criteria", "all.json"), scSorted);
  for (const sc of scSorted) {
    const slug = slugifyRef(sc.ref_id);
    writeJson(path.join(OUT_ROOT, "sc", `${slug}.json`), sc);
    writeJson(path.join(OUT_ROOT, "success-criteria", `${slug}.json`), sc);
  }

  writeJson(path.join(OUT_ROOT, "guidelines", "all.json"), guidelineSorted);
  for (const guideline of guidelineSorted) {
    writeJson(path.join(OUT_ROOT, "guidelines", `${guideline.ref_id}.json`), guideline);
  }

  writeJson(path.join(OUT_ROOT, "techniques", "all.json"), techniqueSorted);
  for (const item of techniqueSorted) {
    writeJson(path.join(OUT_ROOT, "techniques", `${slugifyRef(item.id)}.json`), item);
  }

  writeJson(path.join(OUT_ROOT, "failures", "all.json"), failureSorted);
  for (const item of failureSorted) {
    writeJson(path.join(OUT_ROOT, "failures", `${slugifyRef(item.id)}.json`), item);
  }

  const linkedNodes = [...state.nodesById.values()];
  writeJson(path.join(OUT_ROOT, "linked-data", "all.json"), {
    nodes: linkedNodes,
    edges: state.edges,
  });
}

function main() {
  fs.rmSync(path.join(ROOT, "dist"), { recursive: true, force: true });

  const yamlFiles = walkFiles(ROOT);
  const state = {
    nodesById: new Map(),
    edges: [],
    scRecords: [],
    guidelines: new Map(),
    sufficientTechniques: [],
    advisoryTechniques: [],
    failures: [],
  };

  for (const filePath of yamlFiles) {
    const parsed = loadYaml(filePath);
    if (!parsed) {
      continue;
    }
    const sourcePath = path.relative(ROOT, filePath);
    deepCollectLinkedData(parsed, state, sourcePath);
    extractScFromNormative(filePath, parsed, state);
  }

  extractTechniquesAndFailures(
    path.join(DATA_ROOT, "accessibility-rule-catalogs.yaml"),
    state,
  );

  enrichVersionLinks(state);
  joinScRelationships(state);
  writeEndpoints(state);

  writeText(path.join(OUT_ROOT, "schema.graphql"), SCHEMA_TEXT);
  const introspection = buildIntrospection(SCHEMA_TEXT);
  writeJson(path.join(OUT_ROOT, "introspection.json"), introspection);

  writeJson(path.join(OUT_ROOT, "index.json"), {
    version: "v1",
    generated_at: new Date().toISOString(),
    counts: {
      yaml_files: yamlFiles.length,
      success_criteria: state.scRecords.length,
      guidelines: state.guidelines.size,
      techniques: state.sufficientTechniques.length + state.advisoryTechniques.length,
      failures: state.failures.length,
      linked_nodes: state.nodesById.size,
      linked_edges: state.edges.length,
    },
    endpoints: {
      all_success_criteria: "/api/v1/sc/all.json",
      success_criterion_by_id: "/api/v1/sc/{ref-id}.json",
      guidelines_all: "/api/v1/guidelines/all.json",
      introspection: "/api/v1/introspection.json",
      graphql_schema: "/api/v1/schema.graphql",
    },
  });

  console.log(`YAML files parsed: ${yamlFiles.length}`);
  console.log(`Success criteria: ${state.scRecords.length}`);
  console.log(`Guidelines: ${state.guidelines.size}`);
  console.log(`Techniques: ${state.sufficientTechniques.length + state.advisoryTechniques.length}`);
  console.log(`Failures: ${state.failures.length}`);
  console.log(`Output: ${path.relative(ROOT, OUT_ROOT)}`);
}

main();