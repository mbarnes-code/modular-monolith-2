import process from 'node:process';globalThis._importMeta_=globalThis._importMeta_||{url:"file:///_entry.js",env:process.env};import http, { Server as Server$1 } from 'node:http';
import https, { Server } from 'node:https';
import { EventEmitter } from 'node:events';
import { Buffer as Buffer$1 } from 'node:buffer';
import { promises, existsSync } from 'node:fs';
import { resolve as resolve$1, dirname as dirname$1, join } from 'node:path';
import { createHash } from 'node:crypto';
import { fileURLToPath } from 'node:url';

const suspectProtoRx = /"(?:_|\\u0{2}5[Ff]){2}(?:p|\\u0{2}70)(?:r|\\u0{2}72)(?:o|\\u0{2}6[Ff])(?:t|\\u0{2}74)(?:o|\\u0{2}6[Ff])(?:_|\\u0{2}5[Ff]){2}"\s*:/;
const suspectConstructorRx = /"(?:c|\\u0063)(?:o|\\u006[Ff])(?:n|\\u006[Ee])(?:s|\\u0073)(?:t|\\u0074)(?:r|\\u0072)(?:u|\\u0075)(?:c|\\u0063)(?:t|\\u0074)(?:o|\\u006[Ff])(?:r|\\u0072)"\s*:/;
const JsonSigRx = /^\s*["[{]|^\s*-?\d{1,16}(\.\d{1,17})?([Ee][+-]?\d+)?\s*$/;
function jsonParseTransform(key, value) {
  if (key === "__proto__" || key === "constructor" && value && typeof value === "object" && "prototype" in value) {
    warnKeyDropped(key);
    return;
  }
  return value;
}
function warnKeyDropped(key) {
  console.warn(`[destr] Dropping "${key}" key to prevent prototype pollution.`);
}
function destr(value, options = {}) {
  if (typeof value !== "string") {
    return value;
  }
  if (value[0] === '"' && value[value.length - 1] === '"' && value.indexOf("\\") === -1) {
    return value.slice(1, -1);
  }
  const _value = value.trim();
  if (_value.length <= 9) {
    switch (_value.toLowerCase()) {
      case "true": {
        return true;
      }
      case "false": {
        return false;
      }
      case "undefined": {
        return void 0;
      }
      case "null": {
        return null;
      }
      case "nan": {
        return Number.NaN;
      }
      case "infinity": {
        return Number.POSITIVE_INFINITY;
      }
      case "-infinity": {
        return Number.NEGATIVE_INFINITY;
      }
    }
  }
  if (!JsonSigRx.test(value)) {
    if (options.strict) {
      throw new SyntaxError("[destr] Invalid JSON");
    }
    return value;
  }
  try {
    if (suspectProtoRx.test(value) || suspectConstructorRx.test(value)) {
      if (options.strict) {
        throw new Error("[destr] Possible prototype pollution");
      }
      return JSON.parse(value, jsonParseTransform);
    }
    return JSON.parse(value);
  } catch (error) {
    if (options.strict) {
      throw error;
    }
    return value;
  }
}

const HASH_RE = /#/g;
const AMPERSAND_RE = /&/g;
const SLASH_RE = /\//g;
const EQUAL_RE = /=/g;
const PLUS_RE = /\+/g;
const ENC_CARET_RE = /%5e/gi;
const ENC_BACKTICK_RE = /%60/gi;
const ENC_PIPE_RE = /%7c/gi;
const ENC_SPACE_RE = /%20/gi;
const ENC_SLASH_RE = /%2f/gi;
function encode(text) {
  return encodeURI("" + text).replace(ENC_PIPE_RE, "|");
}
function encodeQueryValue(input) {
  return encode(typeof input === "string" ? input : JSON.stringify(input)).replace(PLUS_RE, "%2B").replace(ENC_SPACE_RE, "+").replace(HASH_RE, "%23").replace(AMPERSAND_RE, "%26").replace(ENC_BACKTICK_RE, "`").replace(ENC_CARET_RE, "^").replace(SLASH_RE, "%2F");
}
function encodeQueryKey(text) {
  return encodeQueryValue(text).replace(EQUAL_RE, "%3D");
}
function decode(text = "") {
  try {
    return decodeURIComponent("" + text);
  } catch {
    return "" + text;
  }
}
function decodePath(text) {
  return decode(text.replace(ENC_SLASH_RE, "%252F"));
}
function decodeQueryKey(text) {
  return decode(text.replace(PLUS_RE, " "));
}
function decodeQueryValue(text) {
  return decode(text.replace(PLUS_RE, " "));
}

function parseQuery(parametersString = "") {
  const object = /* @__PURE__ */ Object.create(null);
  if (parametersString[0] === "?") {
    parametersString = parametersString.slice(1);
  }
  for (const parameter of parametersString.split("&")) {
    const s = parameter.match(/([^=]+)=?(.*)/) || [];
    if (s.length < 2) {
      continue;
    }
    const key = decodeQueryKey(s[1]);
    if (key === "__proto__" || key === "constructor") {
      continue;
    }
    const value = decodeQueryValue(s[2] || "");
    if (object[key] === void 0) {
      object[key] = value;
    } else if (Array.isArray(object[key])) {
      object[key].push(value);
    } else {
      object[key] = [object[key], value];
    }
  }
  return object;
}
function encodeQueryItem(key, value) {
  if (typeof value === "number" || typeof value === "boolean") {
    value = String(value);
  }
  if (!value) {
    return encodeQueryKey(key);
  }
  if (Array.isArray(value)) {
    return value.map(
      (_value) => `${encodeQueryKey(key)}=${encodeQueryValue(_value)}`
    ).join("&");
  }
  return `${encodeQueryKey(key)}=${encodeQueryValue(value)}`;
}
function stringifyQuery(query) {
  return Object.keys(query).filter((k) => query[k] !== void 0).map((k) => encodeQueryItem(k, query[k])).filter(Boolean).join("&");
}

const PROTOCOL_STRICT_REGEX = /^[\s\w\0+.-]{2,}:([/\\]{1,2})/;
const PROTOCOL_REGEX = /^[\s\w\0+.-]{2,}:([/\\]{2})?/;
const PROTOCOL_RELATIVE_REGEX = /^([/\\]\s*){2,}[^/\\]/;
const JOIN_LEADING_SLASH_RE = /^\.?\//;
function hasProtocol(inputString, opts = {}) {
  if (typeof opts === "boolean") {
    opts = { acceptRelative: opts };
  }
  if (opts.strict) {
    return PROTOCOL_STRICT_REGEX.test(inputString);
  }
  return PROTOCOL_REGEX.test(inputString) || (opts.acceptRelative ? PROTOCOL_RELATIVE_REGEX.test(inputString) : false);
}
function hasTrailingSlash(input = "", respectQueryAndFragment) {
  {
    return input.endsWith("/");
  }
}
function withoutTrailingSlash(input = "", respectQueryAndFragment) {
  {
    return (hasTrailingSlash(input) ? input.slice(0, -1) : input) || "/";
  }
}
function withTrailingSlash(input = "", respectQueryAndFragment) {
  {
    return input.endsWith("/") ? input : input + "/";
  }
}
function hasLeadingSlash(input = "") {
  return input.startsWith("/");
}
function withLeadingSlash(input = "") {
  return hasLeadingSlash(input) ? input : "/" + input;
}
function withBase(input, base) {
  if (isEmptyURL(base) || hasProtocol(input)) {
    return input;
  }
  const _base = withoutTrailingSlash(base);
  if (input.startsWith(_base)) {
    return input;
  }
  return joinURL(_base, input);
}
function withoutBase(input, base) {
  if (isEmptyURL(base)) {
    return input;
  }
  const _base = withoutTrailingSlash(base);
  if (!input.startsWith(_base)) {
    return input;
  }
  const trimmed = input.slice(_base.length);
  return trimmed[0] === "/" ? trimmed : "/" + trimmed;
}
function withQuery(input, query) {
  const parsed = parseURL(input);
  const mergedQuery = { ...parseQuery(parsed.search), ...query };
  parsed.search = stringifyQuery(mergedQuery);
  return stringifyParsedURL(parsed);
}
function getQuery$1(input) {
  return parseQuery(parseURL(input).search);
}
function isEmptyURL(url) {
  return !url || url === "/";
}
function isNonEmptyURL(url) {
  return url && url !== "/";
}
function joinURL(base, ...input) {
  let url = base || "";
  for (const segment of input.filter((url2) => isNonEmptyURL(url2))) {
    if (url) {
      const _segment = segment.replace(JOIN_LEADING_SLASH_RE, "");
      url = withTrailingSlash(url) + _segment;
    } else {
      url = segment;
    }
  }
  return url;
}
function joinRelativeURL(..._input) {
  const JOIN_SEGMENT_SPLIT_RE = /\/(?!\/)/;
  const input = _input.filter(Boolean);
  const segments = [];
  let segmentsDepth = 0;
  for (const i of input) {
    if (!i || i === "/") {
      continue;
    }
    for (const [sindex, s] of i.split(JOIN_SEGMENT_SPLIT_RE).entries()) {
      if (!s || s === ".") {
        continue;
      }
      if (s === "..") {
        if (segments.length === 1 && hasProtocol(segments[0])) {
          continue;
        }
        segments.pop();
        segmentsDepth--;
        continue;
      }
      if (sindex === 1 && segments[segments.length - 1]?.endsWith(":/")) {
        segments[segments.length - 1] += "/" + s;
        continue;
      }
      segments.push(s);
      segmentsDepth++;
    }
  }
  let url = segments.join("/");
  if (segmentsDepth >= 0) {
    if (input[0]?.startsWith("/") && !url.startsWith("/")) {
      url = "/" + url;
    } else if (input[0]?.startsWith("./") && !url.startsWith("./")) {
      url = "./" + url;
    }
  } else {
    url = "../".repeat(-1 * segmentsDepth) + url;
  }
  if (input[input.length - 1]?.endsWith("/") && !url.endsWith("/")) {
    url += "/";
  }
  return url;
}

const protocolRelative = Symbol.for("ufo:protocolRelative");
function parseURL(input = "", defaultProto) {
  const _specialProtoMatch = input.match(
    /^[\s\0]*(blob:|data:|javascript:|vbscript:)(.*)/i
  );
  if (_specialProtoMatch) {
    const [, _proto, _pathname = ""] = _specialProtoMatch;
    return {
      protocol: _proto.toLowerCase(),
      pathname: _pathname,
      href: _proto + _pathname,
      auth: "",
      host: "",
      search: "",
      hash: ""
    };
  }
  if (!hasProtocol(input, { acceptRelative: true })) {
    return parsePath(input);
  }
  const [, protocol = "", auth, hostAndPath = ""] = input.replace(/\\/g, "/").match(/^[\s\0]*([\w+.-]{2,}:)?\/\/([^/@]+@)?(.*)/) || [];
  let [, host = "", path = ""] = hostAndPath.match(/([^#/?]*)(.*)?/) || [];
  if (protocol === "file:") {
    path = path.replace(/\/(?=[A-Za-z]:)/, "");
  }
  const { pathname, search, hash } = parsePath(path);
  return {
    protocol: protocol.toLowerCase(),
    auth: auth ? auth.slice(0, Math.max(0, auth.length - 1)) : "",
    host,
    pathname,
    search,
    hash,
    [protocolRelative]: !protocol
  };
}
function parsePath(input = "") {
  const [pathname = "", search = "", hash = ""] = (input.match(/([^#?]*)(\?[^#]*)?(#.*)?/) || []).splice(1);
  return {
    pathname,
    search,
    hash
  };
}
function stringifyParsedURL(parsed) {
  const pathname = parsed.pathname || "";
  const search = parsed.search ? (parsed.search.startsWith("?") ? "" : "?") + parsed.search : "";
  const hash = parsed.hash || "";
  const auth = parsed.auth ? parsed.auth + "@" : "";
  const host = parsed.host || "";
  const proto = parsed.protocol || parsed[protocolRelative] ? (parsed.protocol || "") + "//" : "";
  return proto + auth + host + pathname + search + hash;
}

const NODE_TYPES = {
  NORMAL: 0,
  WILDCARD: 1,
  PLACEHOLDER: 2
};

function createRouter$1(options = {}) {
  const ctx = {
    options,
    rootNode: createRadixNode(),
    staticRoutesMap: {}
  };
  const normalizeTrailingSlash = (p) => options.strictTrailingSlash ? p : p.replace(/\/$/, "") || "/";
  if (options.routes) {
    for (const path in options.routes) {
      insert(ctx, normalizeTrailingSlash(path), options.routes[path]);
    }
  }
  return {
    ctx,
    lookup: (path) => lookup(ctx, normalizeTrailingSlash(path)),
    insert: (path, data) => insert(ctx, normalizeTrailingSlash(path), data),
    remove: (path) => remove(ctx, normalizeTrailingSlash(path))
  };
}
function lookup(ctx, path) {
  const staticPathNode = ctx.staticRoutesMap[path];
  if (staticPathNode) {
    return staticPathNode.data;
  }
  const sections = path.split("/");
  const params = {};
  let paramsFound = false;
  let wildcardNode = null;
  let node = ctx.rootNode;
  let wildCardParam = null;
  for (let i = 0; i < sections.length; i++) {
    const section = sections[i];
    if (node.wildcardChildNode !== null) {
      wildcardNode = node.wildcardChildNode;
      wildCardParam = sections.slice(i).join("/");
    }
    const nextNode = node.children.get(section);
    if (nextNode === void 0) {
      if (node && node.placeholderChildren.length > 1) {
        const remaining = sections.length - i;
        node = node.placeholderChildren.find((c) => c.maxDepth === remaining) || null;
      } else {
        node = node.placeholderChildren[0] || null;
      }
      if (!node) {
        break;
      }
      if (node.paramName) {
        params[node.paramName] = section;
      }
      paramsFound = true;
    } else {
      node = nextNode;
    }
  }
  if ((node === null || node.data === null) && wildcardNode !== null) {
    node = wildcardNode;
    params[node.paramName || "_"] = wildCardParam;
    paramsFound = true;
  }
  if (!node) {
    return null;
  }
  if (paramsFound) {
    return {
      ...node.data,
      params: paramsFound ? params : void 0
    };
  }
  return node.data;
}
function insert(ctx, path, data) {
  let isStaticRoute = true;
  const sections = path.split("/");
  let node = ctx.rootNode;
  let _unnamedPlaceholderCtr = 0;
  const matchedNodes = [node];
  for (const section of sections) {
    let childNode;
    if (childNode = node.children.get(section)) {
      node = childNode;
    } else {
      const type = getNodeType(section);
      childNode = createRadixNode({ type, parent: node });
      node.children.set(section, childNode);
      if (type === NODE_TYPES.PLACEHOLDER) {
        childNode.paramName = section === "*" ? `_${_unnamedPlaceholderCtr++}` : section.slice(1);
        node.placeholderChildren.push(childNode);
        isStaticRoute = false;
      } else if (type === NODE_TYPES.WILDCARD) {
        node.wildcardChildNode = childNode;
        childNode.paramName = section.slice(
          3
          /* "**:" */
        ) || "_";
        isStaticRoute = false;
      }
      matchedNodes.push(childNode);
      node = childNode;
    }
  }
  for (const [depth, node2] of matchedNodes.entries()) {
    node2.maxDepth = Math.max(matchedNodes.length - depth, node2.maxDepth || 0);
  }
  node.data = data;
  if (isStaticRoute === true) {
    ctx.staticRoutesMap[path] = node;
  }
  return node;
}
function remove(ctx, path) {
  let success = false;
  const sections = path.split("/");
  let node = ctx.rootNode;
  for (const section of sections) {
    node = node.children.get(section);
    if (!node) {
      return success;
    }
  }
  if (node.data) {
    const lastSection = sections.at(-1) || "";
    node.data = null;
    if (Object.keys(node.children).length === 0 && node.parent) {
      node.parent.children.delete(lastSection);
      node.parent.wildcardChildNode = null;
      node.parent.placeholderChildren = [];
    }
    success = true;
  }
  return success;
}
function createRadixNode(options = {}) {
  return {
    type: options.type || NODE_TYPES.NORMAL,
    maxDepth: 0,
    parent: options.parent || null,
    children: /* @__PURE__ */ new Map(),
    data: options.data || null,
    paramName: options.paramName || null,
    wildcardChildNode: null,
    placeholderChildren: []
  };
}
function getNodeType(str) {
  if (str.startsWith("**")) {
    return NODE_TYPES.WILDCARD;
  }
  if (str[0] === ":" || str === "*") {
    return NODE_TYPES.PLACEHOLDER;
  }
  return NODE_TYPES.NORMAL;
}

function toRouteMatcher(router) {
  const table = _routerNodeToTable("", router.ctx.rootNode);
  return _createMatcher(table, router.ctx.options.strictTrailingSlash);
}
function _createMatcher(table, strictTrailingSlash) {
  return {
    ctx: { table },
    matchAll: (path) => _matchRoutes(path, table, strictTrailingSlash)
  };
}
function _createRouteTable() {
  return {
    static: /* @__PURE__ */ new Map(),
    wildcard: /* @__PURE__ */ new Map(),
    dynamic: /* @__PURE__ */ new Map()
  };
}
function _matchRoutes(path, table, strictTrailingSlash) {
  if (strictTrailingSlash !== true && path.endsWith("/")) {
    path = path.slice(0, -1) || "/";
  }
  const matches = [];
  for (const [key, value] of _sortRoutesMap(table.wildcard)) {
    if (path === key || path.startsWith(key + "/")) {
      matches.push(value);
    }
  }
  for (const [key, value] of _sortRoutesMap(table.dynamic)) {
    if (path.startsWith(key + "/")) {
      const subPath = "/" + path.slice(key.length).split("/").splice(2).join("/");
      matches.push(..._matchRoutes(subPath, value));
    }
  }
  const staticMatch = table.static.get(path);
  if (staticMatch) {
    matches.push(staticMatch);
  }
  return matches.filter(Boolean);
}
function _sortRoutesMap(m) {
  return [...m.entries()].sort((a, b) => a[0].length - b[0].length);
}
function _routerNodeToTable(initialPath, initialNode) {
  const table = _createRouteTable();
  function _addNode(path, node) {
    if (path) {
      if (node.type === NODE_TYPES.NORMAL && !(path.includes("*") || path.includes(":"))) {
        if (node.data) {
          table.static.set(path, node.data);
        }
      } else if (node.type === NODE_TYPES.WILDCARD) {
        table.wildcard.set(path.replace("/**", ""), node.data);
      } else if (node.type === NODE_TYPES.PLACEHOLDER) {
        const subTable = _routerNodeToTable("", node);
        if (node.data) {
          subTable.static.set("/", node.data);
        }
        table.dynamic.set(path.replace(/\/\*|\/:\w+/, ""), subTable);
        return;
      }
    }
    for (const [childPath, child] of node.children.entries()) {
      _addNode(`${path}/${childPath}`.replace("//", "/"), child);
    }
  }
  _addNode(initialPath, initialNode);
  return table;
}

function isPlainObject(value) {
  if (value === null || typeof value !== "object") {
    return false;
  }
  const prototype = Object.getPrototypeOf(value);
  if (prototype !== null && prototype !== Object.prototype && Object.getPrototypeOf(prototype) !== null) {
    return false;
  }
  if (Symbol.iterator in value) {
    return false;
  }
  if (Symbol.toStringTag in value) {
    return Object.prototype.toString.call(value) === "[object Module]";
  }
  return true;
}

function _defu(baseObject, defaults, namespace = ".", merger) {
  if (!isPlainObject(defaults)) {
    return _defu(baseObject, {}, namespace, merger);
  }
  const object = Object.assign({}, defaults);
  for (const key in baseObject) {
    if (key === "__proto__" || key === "constructor") {
      continue;
    }
    const value = baseObject[key];
    if (value === null || value === void 0) {
      continue;
    }
    if (merger && merger(object, key, value, namespace)) {
      continue;
    }
    if (Array.isArray(value) && Array.isArray(object[key])) {
      object[key] = [...value, ...object[key]];
    } else if (isPlainObject(value) && isPlainObject(object[key])) {
      object[key] = _defu(
        value,
        object[key],
        (namespace ? `${namespace}.` : "") + key.toString(),
        merger
      );
    } else {
      object[key] = value;
    }
  }
  return object;
}
function createDefu(merger) {
  return (...arguments_) => (
    // eslint-disable-next-line unicorn/no-array-reduce
    arguments_.reduce((p, c) => _defu(p, c, "", merger), {})
  );
}
const defu = createDefu();
const defuFn = createDefu((object, key, currentValue) => {
  if (object[key] !== void 0 && typeof currentValue === "function") {
    object[key] = currentValue(object[key]);
    return true;
  }
});

function o(n){throw new Error(`${n} is not implemented yet!`)}let i$1 = class i extends EventEmitter{__unenv__={};readableEncoding=null;readableEnded=true;readableFlowing=false;readableHighWaterMark=0;readableLength=0;readableObjectMode=false;readableAborted=false;readableDidRead=false;closed=false;errored=null;readable=false;destroyed=false;static from(e,t){return new i(t)}constructor(e){super();}_read(e){}read(e){}setEncoding(e){return this}pause(){return this}resume(){return this}isPaused(){return  true}unpipe(e){return this}unshift(e,t){}wrap(e){return this}push(e,t){return  false}_destroy(e,t){this.removeAllListeners();}destroy(e){return this.destroyed=true,this._destroy(e),this}pipe(e,t){return {}}compose(e,t){throw new Error("Method not implemented.")}[Symbol.asyncDispose](){return this.destroy(),Promise.resolve()}async*[Symbol.asyncIterator](){throw o("Readable.asyncIterator")}iterator(e){throw o("Readable.iterator")}map(e,t){throw o("Readable.map")}filter(e,t){throw o("Readable.filter")}forEach(e,t){throw o("Readable.forEach")}reduce(e,t,r){throw o("Readable.reduce")}find(e,t){throw o("Readable.find")}findIndex(e,t){throw o("Readable.findIndex")}some(e,t){throw o("Readable.some")}toArray(e){throw o("Readable.toArray")}every(e,t){throw o("Readable.every")}flatMap(e,t){throw o("Readable.flatMap")}drop(e,t){throw o("Readable.drop")}take(e,t){throw o("Readable.take")}asIndexedPairs(e){throw o("Readable.asIndexedPairs")}};let l$1 = class l extends EventEmitter{__unenv__={};writable=true;writableEnded=false;writableFinished=false;writableHighWaterMark=0;writableLength=0;writableObjectMode=false;writableCorked=0;closed=false;errored=null;writableNeedDrain=false;writableAborted=false;destroyed=false;_data;_encoding="utf8";constructor(e){super();}pipe(e,t){return {}}_write(e,t,r){if(this.writableEnded){r&&r();return}if(this._data===void 0)this._data=e;else {const s=typeof this._data=="string"?Buffer$1.from(this._data,this._encoding||t||"utf8"):this._data,a=typeof e=="string"?Buffer$1.from(e,t||this._encoding||"utf8"):e;this._data=Buffer$1.concat([s,a]);}this._encoding=t,r&&r();}_writev(e,t){}_destroy(e,t){}_final(e){}write(e,t,r){const s=typeof t=="string"?this._encoding:"utf8",a=typeof t=="function"?t:typeof r=="function"?r:void 0;return this._write(e,s,a),true}setDefaultEncoding(e){return this}end(e,t,r){const s=typeof e=="function"?e:typeof t=="function"?t:typeof r=="function"?r:void 0;if(this.writableEnded)return s&&s(),this;const a=e===s?void 0:e;if(a){const u=t===s?void 0:t;this.write(a,u,s);}return this.writableEnded=true,this.writableFinished=true,this.emit("close"),this.emit("finish"),this}cork(){}uncork(){}destroy(e){return this.destroyed=true,delete this._data,this.removeAllListeners(),this}compose(e,t){throw new Error("Method not implemented.")}[Symbol.asyncDispose](){return Promise.resolve()}};const c=class{allowHalfOpen=true;_destroy;constructor(e=new i$1,t=new l$1){Object.assign(this,e),Object.assign(this,t),this._destroy=m(e._destroy,t._destroy);}};function _(){return Object.assign(c.prototype,i$1.prototype),Object.assign(c.prototype,l$1.prototype),c}function m(...n){return function(...e){for(const t of n)t(...e);}}const g=_();class A extends g{__unenv__={};bufferSize=0;bytesRead=0;bytesWritten=0;connecting=false;destroyed=false;pending=false;localAddress="";localPort=0;remoteAddress="";remoteFamily="";remotePort=0;autoSelectFamilyAttemptedAddresses=[];readyState="readOnly";constructor(e){super();}write(e,t,r){return  false}connect(e,t,r){return this}end(e,t,r){return this}setEncoding(e){return this}pause(){return this}resume(){return this}setTimeout(e,t){return this}setNoDelay(e){return this}setKeepAlive(e,t){return this}address(){return {}}unref(){return this}ref(){return this}destroySoon(){this.destroy();}resetAndDestroy(){const e=new Error("ERR_SOCKET_CLOSED");return e.code="ERR_SOCKET_CLOSED",this.destroy(e),this}}class y extends i$1{aborted=false;httpVersion="1.1";httpVersionMajor=1;httpVersionMinor=1;complete=true;connection;socket;headers={};trailers={};method="GET";url="/";statusCode=200;statusMessage="";closed=false;errored=null;readable=false;constructor(e){super(),this.socket=this.connection=e||new A;}get rawHeaders(){const e=this.headers,t=[];for(const r in e)if(Array.isArray(e[r]))for(const s of e[r])t.push(r,s);else t.push(r,e[r]);return t}get rawTrailers(){return []}setTimeout(e,t){return this}get headersDistinct(){return p(this.headers)}get trailersDistinct(){return p(this.trailers)}}function p(n){const e={};for(const[t,r]of Object.entries(n))t&&(e[t]=(Array.isArray(r)?r:[r]).filter(Boolean));return e}class w extends l$1{statusCode=200;statusMessage="";upgrading=false;chunkedEncoding=false;shouldKeepAlive=false;useChunkedEncodingByDefault=false;sendDate=false;finished=false;headersSent=false;strictContentLength=false;connection=null;socket=null;req;_headers={};constructor(e){super(),this.req=e;}assignSocket(e){e._httpMessage=this,this.socket=e,this.connection=e,this.emit("socket",e),this._flush();}_flush(){this.flushHeaders();}detachSocket(e){}writeContinue(e){}writeHead(e,t,r){e&&(this.statusCode=e),typeof t=="string"&&(this.statusMessage=t,t=void 0);const s=r||t;if(s&&!Array.isArray(s))for(const a in s)this.setHeader(a,s[a]);return this.headersSent=true,this}writeProcessing(){}setTimeout(e,t){return this}appendHeader(e,t){e=e.toLowerCase();const r=this._headers[e],s=[...Array.isArray(r)?r:[r],...Array.isArray(t)?t:[t]].filter(Boolean);return this._headers[e]=s.length>1?s:s[0],this}setHeader(e,t){return this._headers[e.toLowerCase()]=t,this}setHeaders(e){for(const[t,r]of Object.entries(e))this.setHeader(t,r);return this}getHeader(e){return this._headers[e.toLowerCase()]}getHeaders(){return this._headers}getHeaderNames(){return Object.keys(this._headers)}hasHeader(e){return e.toLowerCase()in this._headers}removeHeader(e){delete this._headers[e.toLowerCase()];}addTrailers(e){}flushHeaders(){}writeEarlyHints(e,t){typeof t=="function"&&t();}}const E=(()=>{const n=function(){};return n.prototype=Object.create(null),n})();function R(n={}){const e=new E,t=Array.isArray(n)||H(n)?n:Object.entries(n);for(const[r,s]of t)if(s){if(e[r]===void 0){e[r]=s;continue}e[r]=[...Array.isArray(e[r])?e[r]:[e[r]],...Array.isArray(s)?s:[s]];}return e}function H(n){return typeof n?.entries=="function"}function v(n={}){if(n instanceof Headers)return n;const e=new Headers;for(const[t,r]of Object.entries(n))if(r!==void 0){if(Array.isArray(r)){for(const s of r)e.append(t,String(s));continue}e.set(t,String(r));}return e}const S=new Set([101,204,205,304]);async function b(n,e){const t=new y,r=new w(t);t.url=e.url?.toString()||"/";let s;if(!t.url.startsWith("/")){const d=new URL(t.url);s=d.host,t.url=d.pathname+d.search+d.hash;}t.method=e.method||"GET",t.headers=R(e.headers||{}),t.headers.host||(t.headers.host=e.host||s||"localhost"),t.connection.encrypted=t.connection.encrypted||e.protocol==="https",t.body=e.body||null,t.__unenv__=e.context,await n(t,r);let a=r._data;(S.has(r.statusCode)||t.method.toUpperCase()==="HEAD")&&(a=null,delete r._headers["content-length"]);const u={status:r.statusCode,statusText:r.statusMessage,headers:r._headers,body:a};return t.destroy(),r.destroy(),u}async function C(n,e,t={}){try{const r=await b(n,{url:e,...t});return new Response(r.body,{status:r.status,statusText:r.statusText,headers:v(r.headers)})}catch(r){return new Response(r.toString(),{status:Number.parseInt(r.statusCode||r.code)||500,statusText:r.statusText})}}

function hasProp(obj, prop) {
  try {
    return prop in obj;
  } catch {
    return false;
  }
}

class H3Error extends Error {
  static __h3_error__ = true;
  statusCode = 500;
  fatal = false;
  unhandled = false;
  statusMessage;
  data;
  cause;
  constructor(message, opts = {}) {
    super(message, opts);
    if (opts.cause && !this.cause) {
      this.cause = opts.cause;
    }
  }
  toJSON() {
    const obj = {
      message: this.message,
      statusCode: sanitizeStatusCode(this.statusCode, 500)
    };
    if (this.statusMessage) {
      obj.statusMessage = sanitizeStatusMessage(this.statusMessage);
    }
    if (this.data !== void 0) {
      obj.data = this.data;
    }
    return obj;
  }
}
function createError$1(input) {
  if (typeof input === "string") {
    return new H3Error(input);
  }
  if (isError(input)) {
    return input;
  }
  const err = new H3Error(input.message ?? input.statusMessage ?? "", {
    cause: input.cause || input
  });
  if (hasProp(input, "stack")) {
    try {
      Object.defineProperty(err, "stack", {
        get() {
          return input.stack;
        }
      });
    } catch {
      try {
        err.stack = input.stack;
      } catch {
      }
    }
  }
  if (input.data) {
    err.data = input.data;
  }
  if (input.statusCode) {
    err.statusCode = sanitizeStatusCode(input.statusCode, err.statusCode);
  } else if (input.status) {
    err.statusCode = sanitizeStatusCode(input.status, err.statusCode);
  }
  if (input.statusMessage) {
    err.statusMessage = input.statusMessage;
  } else if (input.statusText) {
    err.statusMessage = input.statusText;
  }
  if (err.statusMessage) {
    const originalMessage = err.statusMessage;
    const sanitizedMessage = sanitizeStatusMessage(err.statusMessage);
    if (sanitizedMessage !== originalMessage) {
      console.warn(
        "[h3] Please prefer using `message` for longer error messages instead of `statusMessage`. In the future, `statusMessage` will be sanitized by default."
      );
    }
  }
  if (input.fatal !== void 0) {
    err.fatal = input.fatal;
  }
  if (input.unhandled !== void 0) {
    err.unhandled = input.unhandled;
  }
  return err;
}
function sendError(event, error, debug) {
  if (event.handled) {
    return;
  }
  const h3Error = isError(error) ? error : createError$1(error);
  const responseBody = {
    statusCode: h3Error.statusCode,
    statusMessage: h3Error.statusMessage,
    stack: [],
    data: h3Error.data
  };
  if (debug) {
    responseBody.stack = (h3Error.stack || "").split("\n").map((l) => l.trim());
  }
  if (event.handled) {
    return;
  }
  const _code = Number.parseInt(h3Error.statusCode);
  setResponseStatus(event, _code, h3Error.statusMessage);
  event.node.res.setHeader("content-type", MIMES.json);
  event.node.res.end(JSON.stringify(responseBody, void 0, 2));
}
function isError(input) {
  return input?.constructor?.__h3_error__ === true;
}

function getQuery(event) {
  return getQuery$1(event.path || "");
}
function isMethod(event, expected, allowHead) {
  if (typeof expected === "string") {
    if (event.method === expected) {
      return true;
    }
  } else if (expected.includes(event.method)) {
    return true;
  }
  return false;
}
function assertMethod(event, expected, allowHead) {
  if (!isMethod(event, expected)) {
    throw createError$1({
      statusCode: 405,
      statusMessage: "HTTP method is not allowed."
    });
  }
}
function getRequestHeaders(event) {
  const _headers = {};
  for (const key in event.node.req.headers) {
    const val = event.node.req.headers[key];
    _headers[key] = Array.isArray(val) ? val.filter(Boolean).join(", ") : val;
  }
  return _headers;
}
function getRequestHeader(event, name) {
  const headers = getRequestHeaders(event);
  const value = headers[name.toLowerCase()];
  return value;
}
function getRequestHost(event, opts = {}) {
  if (opts.xForwardedHost) {
    const _header = event.node.req.headers["x-forwarded-host"];
    const xForwardedHost = (_header || "").split(",").shift()?.trim();
    if (xForwardedHost) {
      return xForwardedHost;
    }
  }
  return event.node.req.headers.host || "localhost";
}
function getRequestProtocol(event, opts = {}) {
  if (opts.xForwardedProto !== false && event.node.req.headers["x-forwarded-proto"] === "https") {
    return "https";
  }
  return event.node.req.connection?.encrypted ? "https" : "http";
}
function getRequestURL(event, opts = {}) {
  const host = getRequestHost(event, opts);
  const protocol = getRequestProtocol(event, opts);
  const path = (event.node.req.originalUrl || event.path).replace(
    /^[/\\]+/g,
    "/"
  );
  return new URL(path, `${protocol}://${host}`);
}

const RawBodySymbol = Symbol.for("h3RawBody");
const PayloadMethods$1 = ["PATCH", "POST", "PUT", "DELETE"];
function readRawBody(event, encoding = "utf8") {
  assertMethod(event, PayloadMethods$1);
  const _rawBody = event._requestBody || event.web?.request?.body || event.node.req[RawBodySymbol] || event.node.req.rawBody || event.node.req.body;
  if (_rawBody) {
    const promise2 = Promise.resolve(_rawBody).then((_resolved) => {
      if (Buffer.isBuffer(_resolved)) {
        return _resolved;
      }
      if (typeof _resolved.pipeTo === "function") {
        return new Promise((resolve, reject) => {
          const chunks = [];
          _resolved.pipeTo(
            new WritableStream({
              write(chunk) {
                chunks.push(chunk);
              },
              close() {
                resolve(Buffer.concat(chunks));
              },
              abort(reason) {
                reject(reason);
              }
            })
          ).catch(reject);
        });
      } else if (typeof _resolved.pipe === "function") {
        return new Promise((resolve, reject) => {
          const chunks = [];
          _resolved.on("data", (chunk) => {
            chunks.push(chunk);
          }).on("end", () => {
            resolve(Buffer.concat(chunks));
          }).on("error", reject);
        });
      }
      if (_resolved.constructor === Object) {
        return Buffer.from(JSON.stringify(_resolved));
      }
      if (_resolved instanceof URLSearchParams) {
        return Buffer.from(_resolved.toString());
      }
      if (_resolved instanceof FormData) {
        return new Response(_resolved).bytes().then((uint8arr) => Buffer.from(uint8arr));
      }
      return Buffer.from(_resolved);
    });
    return encoding ? promise2.then((buff) => buff.toString(encoding)) : promise2;
  }
  if (!Number.parseInt(event.node.req.headers["content-length"] || "") && !String(event.node.req.headers["transfer-encoding"] ?? "").split(",").map((e) => e.trim()).filter(Boolean).includes("chunked")) {
    return Promise.resolve(void 0);
  }
  const promise = event.node.req[RawBodySymbol] = new Promise(
    (resolve, reject) => {
      const bodyData = [];
      event.node.req.on("error", (err) => {
        reject(err);
      }).on("data", (chunk) => {
        bodyData.push(chunk);
      }).on("end", () => {
        resolve(Buffer.concat(bodyData));
      });
    }
  );
  const result = encoding ? promise.then((buff) => buff.toString(encoding)) : promise;
  return result;
}
function getRequestWebStream(event) {
  if (!PayloadMethods$1.includes(event.method)) {
    return;
  }
  const bodyStream = event.web?.request?.body || event._requestBody;
  if (bodyStream) {
    return bodyStream;
  }
  const _hasRawBody = RawBodySymbol in event.node.req || "rawBody" in event.node.req || "body" in event.node.req || "__unenv__" in event.node.req;
  if (_hasRawBody) {
    return new ReadableStream({
      async start(controller) {
        const _rawBody = await readRawBody(event, false);
        if (_rawBody) {
          controller.enqueue(_rawBody);
        }
        controller.close();
      }
    });
  }
  return new ReadableStream({
    start: (controller) => {
      event.node.req.on("data", (chunk) => {
        controller.enqueue(chunk);
      });
      event.node.req.on("end", () => {
        controller.close();
      });
      event.node.req.on("error", (err) => {
        controller.error(err);
      });
    }
  });
}

function handleCacheHeaders(event, opts) {
  const cacheControls = ["public", ...opts.cacheControls || []];
  let cacheMatched = false;
  if (opts.maxAge !== void 0) {
    cacheControls.push(`max-age=${+opts.maxAge}`, `s-maxage=${+opts.maxAge}`);
  }
  if (opts.modifiedTime) {
    const modifiedTime = new Date(opts.modifiedTime);
    const ifModifiedSince = event.node.req.headers["if-modified-since"];
    event.node.res.setHeader("last-modified", modifiedTime.toUTCString());
    if (ifModifiedSince && new Date(ifModifiedSince) >= modifiedTime) {
      cacheMatched = true;
    }
  }
  if (opts.etag) {
    event.node.res.setHeader("etag", opts.etag);
    const ifNonMatch = event.node.req.headers["if-none-match"];
    if (ifNonMatch === opts.etag) {
      cacheMatched = true;
    }
  }
  event.node.res.setHeader("cache-control", cacheControls.join(", "));
  if (cacheMatched) {
    event.node.res.statusCode = 304;
    if (!event.handled) {
      event.node.res.end();
    }
    return true;
  }
  return false;
}

const MIMES = {
  html: "text/html",
  json: "application/json"
};

const DISALLOWED_STATUS_CHARS = /[^\u0009\u0020-\u007E]/g;
function sanitizeStatusMessage(statusMessage = "") {
  return statusMessage.replace(DISALLOWED_STATUS_CHARS, "");
}
function sanitizeStatusCode(statusCode, defaultStatusCode = 200) {
  if (!statusCode) {
    return defaultStatusCode;
  }
  if (typeof statusCode === "string") {
    statusCode = Number.parseInt(statusCode, 10);
  }
  if (statusCode < 100 || statusCode > 999) {
    return defaultStatusCode;
  }
  return statusCode;
}
function splitCookiesString(cookiesString) {
  if (Array.isArray(cookiesString)) {
    return cookiesString.flatMap((c) => splitCookiesString(c));
  }
  if (typeof cookiesString !== "string") {
    return [];
  }
  const cookiesStrings = [];
  let pos = 0;
  let start;
  let ch;
  let lastComma;
  let nextStart;
  let cookiesSeparatorFound;
  const skipWhitespace = () => {
    while (pos < cookiesString.length && /\s/.test(cookiesString.charAt(pos))) {
      pos += 1;
    }
    return pos < cookiesString.length;
  };
  const notSpecialChar = () => {
    ch = cookiesString.charAt(pos);
    return ch !== "=" && ch !== ";" && ch !== ",";
  };
  while (pos < cookiesString.length) {
    start = pos;
    cookiesSeparatorFound = false;
    while (skipWhitespace()) {
      ch = cookiesString.charAt(pos);
      if (ch === ",") {
        lastComma = pos;
        pos += 1;
        skipWhitespace();
        nextStart = pos;
        while (pos < cookiesString.length && notSpecialChar()) {
          pos += 1;
        }
        if (pos < cookiesString.length && cookiesString.charAt(pos) === "=") {
          cookiesSeparatorFound = true;
          pos = nextStart;
          cookiesStrings.push(cookiesString.slice(start, lastComma));
          start = pos;
        } else {
          pos = lastComma + 1;
        }
      } else {
        pos += 1;
      }
    }
    if (!cookiesSeparatorFound || pos >= cookiesString.length) {
      cookiesStrings.push(cookiesString.slice(start));
    }
  }
  return cookiesStrings;
}

const defer = typeof setImmediate === "undefined" ? (fn) => fn() : setImmediate;
function send(event, data, type) {
  if (type) {
    defaultContentType(event, type);
  }
  return new Promise((resolve) => {
    defer(() => {
      if (!event.handled) {
        event.node.res.end(data);
      }
      resolve();
    });
  });
}
function sendNoContent(event, code) {
  if (event.handled) {
    return;
  }
  if (!code && event.node.res.statusCode !== 200) {
    code = event.node.res.statusCode;
  }
  const _code = sanitizeStatusCode(code, 204);
  if (_code === 204) {
    event.node.res.removeHeader("content-length");
  }
  event.node.res.writeHead(_code);
  event.node.res.end();
}
function setResponseStatus(event, code, text) {
  if (code) {
    event.node.res.statusCode = sanitizeStatusCode(
      code,
      event.node.res.statusCode
    );
  }
  if (text) {
    event.node.res.statusMessage = sanitizeStatusMessage(text);
  }
}
function getResponseStatus(event) {
  return event.node.res.statusCode;
}
function getResponseStatusText(event) {
  return event.node.res.statusMessage;
}
function defaultContentType(event, type) {
  if (type && event.node.res.statusCode !== 304 && !event.node.res.getHeader("content-type")) {
    event.node.res.setHeader("content-type", type);
  }
}
function sendRedirect(event, location, code = 302) {
  event.node.res.statusCode = sanitizeStatusCode(
    code,
    event.node.res.statusCode
  );
  event.node.res.setHeader("location", location);
  const encodedLoc = location.replace(/"/g, "%22");
  const html = `<!DOCTYPE html><html><head><meta http-equiv="refresh" content="0; url=${encodedLoc}"></head></html>`;
  return send(event, html, MIMES.html);
}
function getResponseHeader(event, name) {
  return event.node.res.getHeader(name);
}
function setResponseHeaders(event, headers) {
  for (const [name, value] of Object.entries(headers)) {
    event.node.res.setHeader(
      name,
      value
    );
  }
}
const setHeaders = setResponseHeaders;
function setResponseHeader(event, name, value) {
  event.node.res.setHeader(name, value);
}
function appendResponseHeader(event, name, value) {
  let current = event.node.res.getHeader(name);
  if (!current) {
    event.node.res.setHeader(name, value);
    return;
  }
  if (!Array.isArray(current)) {
    current = [current.toString()];
  }
  event.node.res.setHeader(name, [...current, value]);
}
function removeResponseHeader(event, name) {
  return event.node.res.removeHeader(name);
}
function isStream(data) {
  if (!data || typeof data !== "object") {
    return false;
  }
  if (typeof data.pipe === "function") {
    if (typeof data._read === "function") {
      return true;
    }
    if (typeof data.abort === "function") {
      return true;
    }
  }
  if (typeof data.pipeTo === "function") {
    return true;
  }
  return false;
}
function isWebResponse(data) {
  return typeof Response !== "undefined" && data instanceof Response;
}
function sendStream(event, stream) {
  if (!stream || typeof stream !== "object") {
    throw new Error("[h3] Invalid stream provided.");
  }
  event.node.res._data = stream;
  if (!event.node.res.socket) {
    event._handled = true;
    return Promise.resolve();
  }
  if (hasProp(stream, "pipeTo") && typeof stream.pipeTo === "function") {
    return stream.pipeTo(
      new WritableStream({
        write(chunk) {
          event.node.res.write(chunk);
        }
      })
    ).then(() => {
      event.node.res.end();
    });
  }
  if (hasProp(stream, "pipe") && typeof stream.pipe === "function") {
    return new Promise((resolve, reject) => {
      stream.pipe(event.node.res);
      if (stream.on) {
        stream.on("end", () => {
          event.node.res.end();
          resolve();
        });
        stream.on("error", (error) => {
          reject(error);
        });
      }
      event.node.res.on("close", () => {
        if (stream.abort) {
          stream.abort();
        }
      });
    });
  }
  throw new Error("[h3] Invalid or incompatible stream provided.");
}
function sendWebResponse(event, response) {
  for (const [key, value] of response.headers) {
    if (key === "set-cookie") {
      event.node.res.appendHeader(key, splitCookiesString(value));
    } else {
      event.node.res.setHeader(key, value);
    }
  }
  if (response.status) {
    event.node.res.statusCode = sanitizeStatusCode(
      response.status,
      event.node.res.statusCode
    );
  }
  if (response.statusText) {
    event.node.res.statusMessage = sanitizeStatusMessage(response.statusText);
  }
  if (response.redirected) {
    event.node.res.setHeader("location", response.url);
  }
  if (!response.body) {
    event.node.res.end();
    return;
  }
  return sendStream(event, response.body);
}

const PayloadMethods = /* @__PURE__ */ new Set(["PATCH", "POST", "PUT", "DELETE"]);
const ignoredHeaders = /* @__PURE__ */ new Set([
  "transfer-encoding",
  "accept-encoding",
  "connection",
  "keep-alive",
  "upgrade",
  "expect",
  "host",
  "accept"
]);
async function proxyRequest(event, target, opts = {}) {
  let body;
  let duplex;
  if (PayloadMethods.has(event.method)) {
    if (opts.streamRequest) {
      body = getRequestWebStream(event);
      duplex = "half";
    } else {
      body = await readRawBody(event, false).catch(() => void 0);
    }
  }
  const method = opts.fetchOptions?.method || event.method;
  const fetchHeaders = mergeHeaders$1(
    getProxyRequestHeaders(event, { host: target.startsWith("/") }),
    opts.fetchOptions?.headers,
    opts.headers
  );
  return sendProxy(event, target, {
    ...opts,
    fetchOptions: {
      method,
      body,
      duplex,
      ...opts.fetchOptions,
      headers: fetchHeaders
    }
  });
}
async function sendProxy(event, target, opts = {}) {
  let response;
  try {
    response = await _getFetch(opts.fetch)(target, {
      headers: opts.headers,
      ignoreResponseError: true,
      // make $ofetch.raw transparent
      ...opts.fetchOptions
    });
  } catch (error) {
    throw createError$1({
      status: 502,
      statusMessage: "Bad Gateway",
      cause: error
    });
  }
  event.node.res.statusCode = sanitizeStatusCode(
    response.status,
    event.node.res.statusCode
  );
  event.node.res.statusMessage = sanitizeStatusMessage(response.statusText);
  const cookies = [];
  for (const [key, value] of response.headers.entries()) {
    if (key === "content-encoding") {
      continue;
    }
    if (key === "content-length") {
      continue;
    }
    if (key === "set-cookie") {
      cookies.push(...splitCookiesString(value));
      continue;
    }
    event.node.res.setHeader(key, value);
  }
  if (cookies.length > 0) {
    event.node.res.setHeader(
      "set-cookie",
      cookies.map((cookie) => {
        if (opts.cookieDomainRewrite) {
          cookie = rewriteCookieProperty(
            cookie,
            opts.cookieDomainRewrite,
            "domain"
          );
        }
        if (opts.cookiePathRewrite) {
          cookie = rewriteCookieProperty(
            cookie,
            opts.cookiePathRewrite,
            "path"
          );
        }
        return cookie;
      })
    );
  }
  if (opts.onResponse) {
    await opts.onResponse(event, response);
  }
  if (response._data !== void 0) {
    return response._data;
  }
  if (event.handled) {
    return;
  }
  if (opts.sendStream === false) {
    const data = new Uint8Array(await response.arrayBuffer());
    return event.node.res.end(data);
  }
  if (response.body) {
    for await (const chunk of response.body) {
      event.node.res.write(chunk);
    }
  }
  return event.node.res.end();
}
function getProxyRequestHeaders(event, opts) {
  const headers = /* @__PURE__ */ Object.create(null);
  const reqHeaders = getRequestHeaders(event);
  for (const name in reqHeaders) {
    if (!ignoredHeaders.has(name) || name === "host" && opts?.host) {
      headers[name] = reqHeaders[name];
    }
  }
  return headers;
}
function fetchWithEvent(event, req, init, options) {
  return _getFetch(options?.fetch)(req, {
    ...init,
    context: init?.context || event.context,
    headers: {
      ...getProxyRequestHeaders(event, {
        host: typeof req === "string" && req.startsWith("/")
      }),
      ...init?.headers
    }
  });
}
function _getFetch(_fetch) {
  if (_fetch) {
    return _fetch;
  }
  if (globalThis.fetch) {
    return globalThis.fetch;
  }
  throw new Error(
    "fetch is not available. Try importing `node-fetch-native/polyfill` for Node.js."
  );
}
function rewriteCookieProperty(header, map, property) {
  const _map = typeof map === "string" ? { "*": map } : map;
  return header.replace(
    new RegExp(`(;\\s*${property}=)([^;]+)`, "gi"),
    (match, prefix, previousValue) => {
      let newValue;
      if (previousValue in _map) {
        newValue = _map[previousValue];
      } else if ("*" in _map) {
        newValue = _map["*"];
      } else {
        return match;
      }
      return newValue ? prefix + newValue : "";
    }
  );
}
function mergeHeaders$1(defaults, ...inputs) {
  const _inputs = inputs.filter(Boolean);
  if (_inputs.length === 0) {
    return defaults;
  }
  const merged = new Headers(defaults);
  for (const input of _inputs) {
    const entries = Array.isArray(input) ? input : typeof input.entries === "function" ? input.entries() : Object.entries(input);
    for (const [key, value] of entries) {
      if (value !== void 0) {
        merged.set(key, value);
      }
    }
  }
  return merged;
}

class H3Event {
  "__is_event__" = true;
  // Context
  node;
  // Node
  web;
  // Web
  context = {};
  // Shared
  // Request
  _method;
  _path;
  _headers;
  _requestBody;
  // Response
  _handled = false;
  // Hooks
  _onBeforeResponseCalled;
  _onAfterResponseCalled;
  constructor(req, res) {
    this.node = { req, res };
  }
  // --- Request ---
  get method() {
    if (!this._method) {
      this._method = (this.node.req.method || "GET").toUpperCase();
    }
    return this._method;
  }
  get path() {
    return this._path || this.node.req.url || "/";
  }
  get headers() {
    if (!this._headers) {
      this._headers = _normalizeNodeHeaders(this.node.req.headers);
    }
    return this._headers;
  }
  // --- Respoonse ---
  get handled() {
    return this._handled || this.node.res.writableEnded || this.node.res.headersSent;
  }
  respondWith(response) {
    return Promise.resolve(response).then(
      (_response) => sendWebResponse(this, _response)
    );
  }
  // --- Utils ---
  toString() {
    return `[${this.method}] ${this.path}`;
  }
  toJSON() {
    return this.toString();
  }
  // --- Deprecated ---
  /** @deprecated Please use `event.node.req` instead. */
  get req() {
    return this.node.req;
  }
  /** @deprecated Please use `event.node.res` instead. */
  get res() {
    return this.node.res;
  }
}
function isEvent(input) {
  return hasProp(input, "__is_event__");
}
function createEvent(req, res) {
  return new H3Event(req, res);
}
function _normalizeNodeHeaders(nodeHeaders) {
  const headers = new Headers();
  for (const [name, value] of Object.entries(nodeHeaders)) {
    if (Array.isArray(value)) {
      for (const item of value) {
        headers.append(name, item);
      }
    } else if (value) {
      headers.set(name, value);
    }
  }
  return headers;
}

function defineEventHandler(handler) {
  if (typeof handler === "function") {
    handler.__is_handler__ = true;
    return handler;
  }
  const _hooks = {
    onRequest: _normalizeArray(handler.onRequest),
    onBeforeResponse: _normalizeArray(handler.onBeforeResponse)
  };
  const _handler = (event) => {
    return _callHandler(event, handler.handler, _hooks);
  };
  _handler.__is_handler__ = true;
  _handler.__resolve__ = handler.handler.__resolve__;
  _handler.__websocket__ = handler.websocket;
  return _handler;
}
function _normalizeArray(input) {
  return input ? Array.isArray(input) ? input : [input] : void 0;
}
async function _callHandler(event, handler, hooks) {
  if (hooks.onRequest) {
    for (const hook of hooks.onRequest) {
      await hook(event);
      if (event.handled) {
        return;
      }
    }
  }
  const body = await handler(event);
  const response = { body };
  if (hooks.onBeforeResponse) {
    for (const hook of hooks.onBeforeResponse) {
      await hook(event, response);
    }
  }
  return response.body;
}
const eventHandler = defineEventHandler;
function isEventHandler(input) {
  return hasProp(input, "__is_handler__");
}
function toEventHandler(input, _, _route) {
  if (!isEventHandler(input)) {
    console.warn(
      "[h3] Implicit event handler conversion is deprecated. Use `eventHandler()` or `fromNodeMiddleware()` to define event handlers.",
      _route && _route !== "/" ? `
     Route: ${_route}` : "",
      `
     Handler: ${input}`
    );
  }
  return input;
}
function defineLazyEventHandler(factory) {
  let _promise;
  let _resolved;
  const resolveHandler = () => {
    if (_resolved) {
      return Promise.resolve(_resolved);
    }
    if (!_promise) {
      _promise = Promise.resolve(factory()).then((r) => {
        const handler2 = r.default || r;
        if (typeof handler2 !== "function") {
          throw new TypeError(
            "Invalid lazy handler result. It should be a function:",
            handler2
          );
        }
        _resolved = { handler: toEventHandler(r.default || r) };
        return _resolved;
      });
    }
    return _promise;
  };
  const handler = eventHandler((event) => {
    if (_resolved) {
      return _resolved.handler(event);
    }
    return resolveHandler().then((r) => r.handler(event));
  });
  handler.__resolve__ = resolveHandler;
  return handler;
}
const lazyEventHandler = defineLazyEventHandler;

function createApp(options = {}) {
  const stack = [];
  const handler = createAppEventHandler(stack, options);
  const resolve = createResolver(stack);
  handler.__resolve__ = resolve;
  const getWebsocket = cachedFn(() => websocketOptions(resolve, options));
  const app = {
    // @ts-expect-error
    use: (arg1, arg2, arg3) => use(app, arg1, arg2, arg3),
    resolve,
    handler,
    stack,
    options,
    get websocket() {
      return getWebsocket();
    }
  };
  return app;
}
function use(app, arg1, arg2, arg3) {
  if (Array.isArray(arg1)) {
    for (const i of arg1) {
      use(app, i, arg2, arg3);
    }
  } else if (Array.isArray(arg2)) {
    for (const i of arg2) {
      use(app, arg1, i, arg3);
    }
  } else if (typeof arg1 === "string") {
    app.stack.push(
      normalizeLayer({ ...arg3, route: arg1, handler: arg2 })
    );
  } else if (typeof arg1 === "function") {
    app.stack.push(normalizeLayer({ ...arg2, handler: arg1 }));
  } else {
    app.stack.push(normalizeLayer({ ...arg1 }));
  }
  return app;
}
function createAppEventHandler(stack, options) {
  const spacing = options.debug ? 2 : void 0;
  return eventHandler(async (event) => {
    event.node.req.originalUrl = event.node.req.originalUrl || event.node.req.url || "/";
    const _reqPath = event._path || event.node.req.url || "/";
    let _layerPath;
    if (options.onRequest) {
      await options.onRequest(event);
    }
    for (const layer of stack) {
      if (layer.route.length > 1) {
        if (!_reqPath.startsWith(layer.route)) {
          continue;
        }
        _layerPath = _reqPath.slice(layer.route.length) || "/";
      } else {
        _layerPath = _reqPath;
      }
      if (layer.match && !layer.match(_layerPath, event)) {
        continue;
      }
      event._path = _layerPath;
      event.node.req.url = _layerPath;
      const val = await layer.handler(event);
      const _body = val === void 0 ? void 0 : await val;
      if (_body !== void 0) {
        const _response = { body: _body };
        if (options.onBeforeResponse) {
          event._onBeforeResponseCalled = true;
          await options.onBeforeResponse(event, _response);
        }
        await handleHandlerResponse(event, _response.body, spacing);
        if (options.onAfterResponse) {
          event._onAfterResponseCalled = true;
          await options.onAfterResponse(event, _response);
        }
        return;
      }
      if (event.handled) {
        if (options.onAfterResponse) {
          event._onAfterResponseCalled = true;
          await options.onAfterResponse(event, void 0);
        }
        return;
      }
    }
    if (!event.handled) {
      throw createError$1({
        statusCode: 404,
        statusMessage: `Cannot find any path matching ${event.path || "/"}.`
      });
    }
    if (options.onAfterResponse) {
      event._onAfterResponseCalled = true;
      await options.onAfterResponse(event, void 0);
    }
  });
}
function createResolver(stack) {
  return async (path) => {
    let _layerPath;
    for (const layer of stack) {
      if (layer.route === "/" && !layer.handler.__resolve__) {
        continue;
      }
      if (!path.startsWith(layer.route)) {
        continue;
      }
      _layerPath = path.slice(layer.route.length) || "/";
      if (layer.match && !layer.match(_layerPath, void 0)) {
        continue;
      }
      let res = { route: layer.route, handler: layer.handler };
      if (res.handler.__resolve__) {
        const _res = await res.handler.__resolve__(_layerPath);
        if (!_res) {
          continue;
        }
        res = {
          ...res,
          ..._res,
          route: joinURL(res.route || "/", _res.route || "/")
        };
      }
      return res;
    }
  };
}
function normalizeLayer(input) {
  let handler = input.handler;
  if (handler.handler) {
    handler = handler.handler;
  }
  if (input.lazy) {
    handler = lazyEventHandler(handler);
  } else if (!isEventHandler(handler)) {
    handler = toEventHandler(handler, void 0, input.route);
  }
  return {
    route: withoutTrailingSlash(input.route),
    match: input.match,
    handler
  };
}
function handleHandlerResponse(event, val, jsonSpace) {
  if (val === null) {
    return sendNoContent(event);
  }
  if (val) {
    if (isWebResponse(val)) {
      return sendWebResponse(event, val);
    }
    if (isStream(val)) {
      return sendStream(event, val);
    }
    if (val.buffer) {
      return send(event, val);
    }
    if (val.arrayBuffer && typeof val.arrayBuffer === "function") {
      return val.arrayBuffer().then((arrayBuffer) => {
        return send(event, Buffer.from(arrayBuffer), val.type);
      });
    }
    if (val instanceof Error) {
      throw createError$1(val);
    }
    if (typeof val.end === "function") {
      return true;
    }
  }
  const valType = typeof val;
  if (valType === "string") {
    return send(event, val, MIMES.html);
  }
  if (valType === "object" || valType === "boolean" || valType === "number") {
    return send(event, JSON.stringify(val, void 0, jsonSpace), MIMES.json);
  }
  if (valType === "bigint") {
    return send(event, val.toString(), MIMES.json);
  }
  throw createError$1({
    statusCode: 500,
    statusMessage: `[h3] Cannot send ${valType} as response.`
  });
}
function cachedFn(fn) {
  let cache;
  return () => {
    if (!cache) {
      cache = fn();
    }
    return cache;
  };
}
function websocketOptions(evResolver, appOptions) {
  return {
    ...appOptions.websocket,
    async resolve(info) {
      const url = info.request?.url || info.url || "/";
      const { pathname } = typeof url === "string" ? parseURL(url) : url;
      const resolved = await evResolver(pathname);
      return resolved?.handler?.__websocket__ || {};
    }
  };
}

const RouterMethods = [
  "connect",
  "delete",
  "get",
  "head",
  "options",
  "post",
  "put",
  "trace",
  "patch"
];
function createRouter(opts = {}) {
  const _router = createRouter$1({});
  const routes = {};
  let _matcher;
  const router = {};
  const addRoute = (path, handler, method) => {
    let route = routes[path];
    if (!route) {
      routes[path] = route = { path, handlers: {} };
      _router.insert(path, route);
    }
    if (Array.isArray(method)) {
      for (const m of method) {
        addRoute(path, handler, m);
      }
    } else {
      route.handlers[method] = toEventHandler(handler, void 0, path);
    }
    return router;
  };
  router.use = router.add = (path, handler, method) => addRoute(path, handler, method || "all");
  for (const method of RouterMethods) {
    router[method] = (path, handle) => router.add(path, handle, method);
  }
  const matchHandler = (path = "/", method = "get") => {
    const qIndex = path.indexOf("?");
    if (qIndex !== -1) {
      path = path.slice(0, Math.max(0, qIndex));
    }
    const matched = _router.lookup(path);
    if (!matched || !matched.handlers) {
      return {
        error: createError$1({
          statusCode: 404,
          name: "Not Found",
          statusMessage: `Cannot find any route matching ${path || "/"}.`
        })
      };
    }
    let handler = matched.handlers[method] || matched.handlers.all;
    if (!handler) {
      if (!_matcher) {
        _matcher = toRouteMatcher(_router);
      }
      const _matches = _matcher.matchAll(path).reverse();
      for (const _match of _matches) {
        if (_match.handlers[method]) {
          handler = _match.handlers[method];
          matched.handlers[method] = matched.handlers[method] || handler;
          break;
        }
        if (_match.handlers.all) {
          handler = _match.handlers.all;
          matched.handlers.all = matched.handlers.all || handler;
          break;
        }
      }
    }
    if (!handler) {
      return {
        error: createError$1({
          statusCode: 405,
          name: "Method Not Allowed",
          statusMessage: `Method ${method} is not allowed on this route.`
        })
      };
    }
    return { matched, handler };
  };
  const isPreemptive = opts.preemptive || opts.preemtive;
  router.handler = eventHandler((event) => {
    const match = matchHandler(
      event.path,
      event.method.toLowerCase()
    );
    if ("error" in match) {
      if (isPreemptive) {
        throw match.error;
      } else {
        return;
      }
    }
    event.context.matchedRoute = match.matched;
    const params = match.matched.params || {};
    event.context.params = params;
    return Promise.resolve(match.handler(event)).then((res) => {
      if (res === void 0 && isPreemptive) {
        return null;
      }
      return res;
    });
  });
  router.handler.__resolve__ = async (path) => {
    path = withLeadingSlash(path);
    const match = matchHandler(path);
    if ("error" in match) {
      return;
    }
    let res = {
      route: match.matched.path,
      handler: match.handler
    };
    if (match.handler.__resolve__) {
      const _res = await match.handler.__resolve__(path);
      if (!_res) {
        return;
      }
      res = { ...res, ..._res };
    }
    return res;
  };
  return router;
}
function toNodeListener(app) {
  const toNodeHandle = async function(req, res) {
    const event = createEvent(req, res);
    try {
      await app.handler(event);
    } catch (_error) {
      const error = createError$1(_error);
      if (!isError(_error)) {
        error.unhandled = true;
      }
      setResponseStatus(event, error.statusCode, error.statusMessage);
      if (app.options.onError) {
        await app.options.onError(error, event);
      }
      if (event.handled) {
        return;
      }
      if (error.unhandled || error.fatal) {
        console.error("[h3]", error.fatal ? "[fatal]" : "[unhandled]", error);
      }
      if (app.options.onBeforeResponse && !event._onBeforeResponseCalled) {
        await app.options.onBeforeResponse(event, { body: error });
      }
      await sendError(event, error, !!app.options.debug);
      if (app.options.onAfterResponse && !event._onAfterResponseCalled) {
        await app.options.onAfterResponse(event, { body: error });
      }
    }
  };
  return toNodeHandle;
}

function flatHooks(configHooks, hooks = {}, parentName) {
  for (const key in configHooks) {
    const subHook = configHooks[key];
    const name = parentName ? `${parentName}:${key}` : key;
    if (typeof subHook === "object" && subHook !== null) {
      flatHooks(subHook, hooks, name);
    } else if (typeof subHook === "function") {
      hooks[name] = subHook;
    }
  }
  return hooks;
}
const defaultTask = { run: (function_) => function_() };
const _createTask = () => defaultTask;
const createTask = typeof console.createTask !== "undefined" ? console.createTask : _createTask;
function serialTaskCaller(hooks, args) {
  const name = args.shift();
  const task = createTask(name);
  return hooks.reduce(
    (promise, hookFunction) => promise.then(() => task.run(() => hookFunction(...args))),
    Promise.resolve()
  );
}
function parallelTaskCaller(hooks, args) {
  const name = args.shift();
  const task = createTask(name);
  return Promise.all(hooks.map((hook) => task.run(() => hook(...args))));
}
function callEachWith(callbacks, arg0) {
  for (const callback of [...callbacks]) {
    callback(arg0);
  }
}

class Hookable {
  constructor() {
    this._hooks = {};
    this._before = void 0;
    this._after = void 0;
    this._deprecatedMessages = void 0;
    this._deprecatedHooks = {};
    this.hook = this.hook.bind(this);
    this.callHook = this.callHook.bind(this);
    this.callHookWith = this.callHookWith.bind(this);
  }
  hook(name, function_, options = {}) {
    if (!name || typeof function_ !== "function") {
      return () => {
      };
    }
    const originalName = name;
    let dep;
    while (this._deprecatedHooks[name]) {
      dep = this._deprecatedHooks[name];
      name = dep.to;
    }
    if (dep && !options.allowDeprecated) {
      let message = dep.message;
      if (!message) {
        message = `${originalName} hook has been deprecated` + (dep.to ? `, please use ${dep.to}` : "");
      }
      if (!this._deprecatedMessages) {
        this._deprecatedMessages = /* @__PURE__ */ new Set();
      }
      if (!this._deprecatedMessages.has(message)) {
        console.warn(message);
        this._deprecatedMessages.add(message);
      }
    }
    if (!function_.name) {
      try {
        Object.defineProperty(function_, "name", {
          get: () => "_" + name.replace(/\W+/g, "_") + "_hook_cb",
          configurable: true
        });
      } catch {
      }
    }
    this._hooks[name] = this._hooks[name] || [];
    this._hooks[name].push(function_);
    return () => {
      if (function_) {
        this.removeHook(name, function_);
        function_ = void 0;
      }
    };
  }
  hookOnce(name, function_) {
    let _unreg;
    let _function = (...arguments_) => {
      if (typeof _unreg === "function") {
        _unreg();
      }
      _unreg = void 0;
      _function = void 0;
      return function_(...arguments_);
    };
    _unreg = this.hook(name, _function);
    return _unreg;
  }
  removeHook(name, function_) {
    if (this._hooks[name]) {
      const index = this._hooks[name].indexOf(function_);
      if (index !== -1) {
        this._hooks[name].splice(index, 1);
      }
      if (this._hooks[name].length === 0) {
        delete this._hooks[name];
      }
    }
  }
  deprecateHook(name, deprecated) {
    this._deprecatedHooks[name] = typeof deprecated === "string" ? { to: deprecated } : deprecated;
    const _hooks = this._hooks[name] || [];
    delete this._hooks[name];
    for (const hook of _hooks) {
      this.hook(name, hook);
    }
  }
  deprecateHooks(deprecatedHooks) {
    Object.assign(this._deprecatedHooks, deprecatedHooks);
    for (const name in deprecatedHooks) {
      this.deprecateHook(name, deprecatedHooks[name]);
    }
  }
  addHooks(configHooks) {
    const hooks = flatHooks(configHooks);
    const removeFns = Object.keys(hooks).map(
      (key) => this.hook(key, hooks[key])
    );
    return () => {
      for (const unreg of removeFns.splice(0, removeFns.length)) {
        unreg();
      }
    };
  }
  removeHooks(configHooks) {
    const hooks = flatHooks(configHooks);
    for (const key in hooks) {
      this.removeHook(key, hooks[key]);
    }
  }
  removeAllHooks() {
    for (const key in this._hooks) {
      delete this._hooks[key];
    }
  }
  callHook(name, ...arguments_) {
    arguments_.unshift(name);
    return this.callHookWith(serialTaskCaller, name, ...arguments_);
  }
  callHookParallel(name, ...arguments_) {
    arguments_.unshift(name);
    return this.callHookWith(parallelTaskCaller, name, ...arguments_);
  }
  callHookWith(caller, name, ...arguments_) {
    const event = this._before || this._after ? { name, args: arguments_, context: {} } : void 0;
    if (this._before) {
      callEachWith(this._before, event);
    }
    const result = caller(
      name in this._hooks ? [...this._hooks[name]] : [],
      arguments_
    );
    if (result instanceof Promise) {
      return result.finally(() => {
        if (this._after && event) {
          callEachWith(this._after, event);
        }
      });
    }
    if (this._after && event) {
      callEachWith(this._after, event);
    }
    return result;
  }
  beforeEach(function_) {
    this._before = this._before || [];
    this._before.push(function_);
    return () => {
      if (this._before !== void 0) {
        const index = this._before.indexOf(function_);
        if (index !== -1) {
          this._before.splice(index, 1);
        }
      }
    };
  }
  afterEach(function_) {
    this._after = this._after || [];
    this._after.push(function_);
    return () => {
      if (this._after !== void 0) {
        const index = this._after.indexOf(function_);
        if (index !== -1) {
          this._after.splice(index, 1);
        }
      }
    };
  }
}
function createHooks() {
  return new Hookable();
}

const s$1=globalThis.Headers,i=globalThis.AbortController,l=globalThis.fetch||(()=>{throw new Error("[node-fetch-native] Failed to fetch: `globalThis.fetch` is not available!")});

class FetchError extends Error {
  constructor(message, opts) {
    super(message, opts);
    this.name = "FetchError";
    if (opts?.cause && !this.cause) {
      this.cause = opts.cause;
    }
  }
}
function createFetchError(ctx) {
  const errorMessage = ctx.error?.message || ctx.error?.toString() || "";
  const method = ctx.request?.method || ctx.options?.method || "GET";
  const url = ctx.request?.url || String(ctx.request) || "/";
  const requestStr = `[${method}] ${JSON.stringify(url)}`;
  const statusStr = ctx.response ? `${ctx.response.status} ${ctx.response.statusText}` : "<no response>";
  const message = `${requestStr}: ${statusStr}${errorMessage ? ` ${errorMessage}` : ""}`;
  const fetchError = new FetchError(
    message,
    ctx.error ? { cause: ctx.error } : void 0
  );
  for (const key of ["request", "options", "response"]) {
    Object.defineProperty(fetchError, key, {
      get() {
        return ctx[key];
      }
    });
  }
  for (const [key, refKey] of [
    ["data", "_data"],
    ["status", "status"],
    ["statusCode", "status"],
    ["statusText", "statusText"],
    ["statusMessage", "statusText"]
  ]) {
    Object.defineProperty(fetchError, key, {
      get() {
        return ctx.response && ctx.response[refKey];
      }
    });
  }
  return fetchError;
}

const payloadMethods = new Set(
  Object.freeze(["PATCH", "POST", "PUT", "DELETE"])
);
function isPayloadMethod(method = "GET") {
  return payloadMethods.has(method.toUpperCase());
}
function isJSONSerializable(value) {
  if (value === void 0) {
    return false;
  }
  const t = typeof value;
  if (t === "string" || t === "number" || t === "boolean" || t === null) {
    return true;
  }
  if (t !== "object") {
    return false;
  }
  if (Array.isArray(value)) {
    return true;
  }
  if (value.buffer) {
    return false;
  }
  if (value instanceof FormData || value instanceof URLSearchParams) {
    return false;
  }
  return value.constructor && value.constructor.name === "Object" || typeof value.toJSON === "function";
}
const textTypes = /* @__PURE__ */ new Set([
  "image/svg",
  "application/xml",
  "application/xhtml",
  "application/html"
]);
const JSON_RE = /^application\/(?:[\w!#$%&*.^`~-]*\+)?json(;.+)?$/i;
function detectResponseType(_contentType = "") {
  if (!_contentType) {
    return "json";
  }
  const contentType = _contentType.split(";").shift() || "";
  if (JSON_RE.test(contentType)) {
    return "json";
  }
  if (contentType === "text/event-stream") {
    return "stream";
  }
  if (textTypes.has(contentType) || contentType.startsWith("text/")) {
    return "text";
  }
  return "blob";
}
function resolveFetchOptions(request, input, defaults, Headers) {
  const headers = mergeHeaders(
    input?.headers ?? request?.headers,
    defaults?.headers,
    Headers
  );
  let query;
  if (defaults?.query || defaults?.params || input?.params || input?.query) {
    query = {
      ...defaults?.params,
      ...defaults?.query,
      ...input?.params,
      ...input?.query
    };
  }
  return {
    ...defaults,
    ...input,
    query,
    params: query,
    headers
  };
}
function mergeHeaders(input, defaults, Headers) {
  if (!defaults) {
    return new Headers(input);
  }
  const headers = new Headers(defaults);
  if (input) {
    for (const [key, value] of Symbol.iterator in input || Array.isArray(input) ? input : new Headers(input)) {
      headers.set(key, value);
    }
  }
  return headers;
}
async function callHooks(context, hooks) {
  if (hooks) {
    if (Array.isArray(hooks)) {
      for (const hook of hooks) {
        await hook(context);
      }
    } else {
      await hooks(context);
    }
  }
}

const retryStatusCodes = /* @__PURE__ */ new Set([
  408,
  // Request Timeout
  409,
  // Conflict
  425,
  // Too Early (Experimental)
  429,
  // Too Many Requests
  500,
  // Internal Server Error
  502,
  // Bad Gateway
  503,
  // Service Unavailable
  504
  // Gateway Timeout
]);
const nullBodyResponses = /* @__PURE__ */ new Set([101, 204, 205, 304]);
function createFetch(globalOptions = {}) {
  const {
    fetch = globalThis.fetch,
    Headers = globalThis.Headers,
    AbortController = globalThis.AbortController
  } = globalOptions;
  async function onError(context) {
    const isAbort = context.error && context.error.name === "AbortError" && !context.options.timeout || false;
    if (context.options.retry !== false && !isAbort) {
      let retries;
      if (typeof context.options.retry === "number") {
        retries = context.options.retry;
      } else {
        retries = isPayloadMethod(context.options.method) ? 0 : 1;
      }
      const responseCode = context.response && context.response.status || 500;
      if (retries > 0 && (Array.isArray(context.options.retryStatusCodes) ? context.options.retryStatusCodes.includes(responseCode) : retryStatusCodes.has(responseCode))) {
        const retryDelay = typeof context.options.retryDelay === "function" ? context.options.retryDelay(context) : context.options.retryDelay || 0;
        if (retryDelay > 0) {
          await new Promise((resolve) => setTimeout(resolve, retryDelay));
        }
        return $fetchRaw(context.request, {
          ...context.options,
          retry: retries - 1
        });
      }
    }
    const error = createFetchError(context);
    if (Error.captureStackTrace) {
      Error.captureStackTrace(error, $fetchRaw);
    }
    throw error;
  }
  const $fetchRaw = async function $fetchRaw2(_request, _options = {}) {
    const context = {
      request: _request,
      options: resolveFetchOptions(
        _request,
        _options,
        globalOptions.defaults,
        Headers
      ),
      response: void 0,
      error: void 0
    };
    if (context.options.method) {
      context.options.method = context.options.method.toUpperCase();
    }
    if (context.options.onRequest) {
      await callHooks(context, context.options.onRequest);
      if (!(context.options.headers instanceof Headers)) {
        context.options.headers = new Headers(
          context.options.headers || {}
          /* compat */
        );
      }
    }
    if (typeof context.request === "string") {
      if (context.options.baseURL) {
        context.request = withBase(context.request, context.options.baseURL);
      }
      if (context.options.query) {
        context.request = withQuery(context.request, context.options.query);
        delete context.options.query;
      }
      if ("query" in context.options) {
        delete context.options.query;
      }
      if ("params" in context.options) {
        delete context.options.params;
      }
    }
    if (context.options.body && isPayloadMethod(context.options.method)) {
      if (isJSONSerializable(context.options.body)) {
        const contentType = context.options.headers.get("content-type");
        if (typeof context.options.body !== "string") {
          context.options.body = contentType === "application/x-www-form-urlencoded" ? new URLSearchParams(
            context.options.body
          ).toString() : JSON.stringify(context.options.body);
        }
        if (!contentType) {
          context.options.headers.set("content-type", "application/json");
        }
        if (!context.options.headers.has("accept")) {
          context.options.headers.set("accept", "application/json");
        }
      } else if (
        // ReadableStream Body
        "pipeTo" in context.options.body && typeof context.options.body.pipeTo === "function" || // Node.js Stream Body
        typeof context.options.body.pipe === "function"
      ) {
        if (!("duplex" in context.options)) {
          context.options.duplex = "half";
        }
      }
    }
    let abortTimeout;
    if (!context.options.signal && context.options.timeout) {
      const controller = new AbortController();
      abortTimeout = setTimeout(() => {
        const error = new Error(
          "[TimeoutError]: The operation was aborted due to timeout"
        );
        error.name = "TimeoutError";
        error.code = 23;
        controller.abort(error);
      }, context.options.timeout);
      context.options.signal = controller.signal;
    }
    try {
      context.response = await fetch(
        context.request,
        context.options
      );
    } catch (error) {
      context.error = error;
      if (context.options.onRequestError) {
        await callHooks(
          context,
          context.options.onRequestError
        );
      }
      return await onError(context);
    } finally {
      if (abortTimeout) {
        clearTimeout(abortTimeout);
      }
    }
    const hasBody = (context.response.body || // https://github.com/unjs/ofetch/issues/324
    // https://github.com/unjs/ofetch/issues/294
    // https://github.com/JakeChampion/fetch/issues/1454
    context.response._bodyInit) && !nullBodyResponses.has(context.response.status) && context.options.method !== "HEAD";
    if (hasBody) {
      const responseType = (context.options.parseResponse ? "json" : context.options.responseType) || detectResponseType(context.response.headers.get("content-type") || "");
      switch (responseType) {
        case "json": {
          const data = await context.response.text();
          const parseFunction = context.options.parseResponse || destr;
          context.response._data = parseFunction(data);
          break;
        }
        case "stream": {
          context.response._data = context.response.body || context.response._bodyInit;
          break;
        }
        default: {
          context.response._data = await context.response[responseType]();
        }
      }
    }
    if (context.options.onResponse) {
      await callHooks(
        context,
        context.options.onResponse
      );
    }
    if (!context.options.ignoreResponseError && context.response.status >= 400 && context.response.status < 600) {
      if (context.options.onResponseError) {
        await callHooks(
          context,
          context.options.onResponseError
        );
      }
      return await onError(context);
    }
    return context.response;
  };
  const $fetch = async function $fetch2(request, options) {
    const r = await $fetchRaw(request, options);
    return r._data;
  };
  $fetch.raw = $fetchRaw;
  $fetch.native = (...args) => fetch(...args);
  $fetch.create = (defaultOptions = {}, customGlobalOptions = {}) => createFetch({
    ...globalOptions,
    ...customGlobalOptions,
    defaults: {
      ...globalOptions.defaults,
      ...customGlobalOptions.defaults,
      ...defaultOptions
    }
  });
  return $fetch;
}

function createNodeFetch() {
  const useKeepAlive = JSON.parse(process.env.FETCH_KEEP_ALIVE || "false");
  if (!useKeepAlive) {
    return l;
  }
  const agentOptions = { keepAlive: true };
  const httpAgent = new http.Agent(agentOptions);
  const httpsAgent = new https.Agent(agentOptions);
  const nodeFetchOptions = {
    agent(parsedURL) {
      return parsedURL.protocol === "http:" ? httpAgent : httpsAgent;
    }
  };
  return function nodeFetchWithKeepAlive(input, init) {
    return l(input, { ...nodeFetchOptions, ...init });
  };
}
const fetch = globalThis.fetch ? (...args) => globalThis.fetch(...args) : createNodeFetch();
const Headers$1 = globalThis.Headers || s$1;
const AbortController = globalThis.AbortController || i;
createFetch({ fetch, Headers: Headers$1, AbortController });

function wrapToPromise(value) {
  if (!value || typeof value.then !== "function") {
    return Promise.resolve(value);
  }
  return value;
}
function asyncCall(function_, ...arguments_) {
  try {
    return wrapToPromise(function_(...arguments_));
  } catch (error) {
    return Promise.reject(error);
  }
}
function isPrimitive(value) {
  const type = typeof value;
  return value === null || type !== "object" && type !== "function";
}
function isPureObject(value) {
  const proto = Object.getPrototypeOf(value);
  return !proto || proto.isPrototypeOf(Object);
}
function stringify(value) {
  if (isPrimitive(value)) {
    return String(value);
  }
  if (isPureObject(value) || Array.isArray(value)) {
    return JSON.stringify(value);
  }
  if (typeof value.toJSON === "function") {
    return stringify(value.toJSON());
  }
  throw new Error("[unstorage] Cannot stringify value!");
}
const BASE64_PREFIX = "base64:";
function serializeRaw(value) {
  if (typeof value === "string") {
    return value;
  }
  return BASE64_PREFIX + base64Encode(value);
}
function deserializeRaw(value) {
  if (typeof value !== "string") {
    return value;
  }
  if (!value.startsWith(BASE64_PREFIX)) {
    return value;
  }
  return base64Decode(value.slice(BASE64_PREFIX.length));
}
function base64Decode(input) {
  if (globalThis.Buffer) {
    return Buffer.from(input, "base64");
  }
  return Uint8Array.from(
    globalThis.atob(input),
    (c) => c.codePointAt(0)
  );
}
function base64Encode(input) {
  if (globalThis.Buffer) {
    return Buffer.from(input).toString("base64");
  }
  return globalThis.btoa(String.fromCodePoint(...input));
}

const storageKeyProperties = [
  "has",
  "hasItem",
  "get",
  "getItem",
  "getItemRaw",
  "set",
  "setItem",
  "setItemRaw",
  "del",
  "remove",
  "removeItem",
  "getMeta",
  "setMeta",
  "removeMeta",
  "getKeys",
  "clear",
  "mount",
  "unmount"
];
function prefixStorage(storage, base) {
  base = normalizeBaseKey(base);
  if (!base) {
    return storage;
  }
  const nsStorage = { ...storage };
  for (const property of storageKeyProperties) {
    nsStorage[property] = (key = "", ...args) => (
      // @ts-ignore
      storage[property](base + key, ...args)
    );
  }
  nsStorage.getKeys = (key = "", ...arguments_) => storage.getKeys(base + key, ...arguments_).then((keys) => keys.map((key2) => key2.slice(base.length)));
  nsStorage.keys = nsStorage.getKeys;
  nsStorage.getItems = async (items, commonOptions) => {
    const prefixedItems = items.map(
      (item) => typeof item === "string" ? base + item : { ...item, key: base + item.key }
    );
    const results = await storage.getItems(prefixedItems, commonOptions);
    return results.map((entry) => ({
      key: entry.key.slice(base.length),
      value: entry.value
    }));
  };
  nsStorage.setItems = async (items, commonOptions) => {
    const prefixedItems = items.map((item) => ({
      key: base + item.key,
      value: item.value,
      options: item.options
    }));
    return storage.setItems(prefixedItems, commonOptions);
  };
  return nsStorage;
}
function normalizeKey$1(key) {
  if (!key) {
    return "";
  }
  return key.split("?")[0]?.replace(/[/\\]/g, ":").replace(/:+/g, ":").replace(/^:|:$/g, "") || "";
}
function joinKeys(...keys) {
  return normalizeKey$1(keys.join(":"));
}
function normalizeBaseKey(base) {
  base = normalizeKey$1(base);
  return base ? base + ":" : "";
}
function filterKeyByDepth(key, depth) {
  if (depth === void 0) {
    return true;
  }
  let substrCount = 0;
  let index = key.indexOf(":");
  while (index > -1) {
    substrCount++;
    index = key.indexOf(":", index + 1);
  }
  return substrCount <= depth;
}
function filterKeyByBase(key, base) {
  if (base) {
    return key.startsWith(base) && key[key.length - 1] !== "$";
  }
  return key[key.length - 1] !== "$";
}

function defineDriver$1(factory) {
  return factory;
}

const DRIVER_NAME$1 = "memory";
const memory = defineDriver$1(() => {
  const data = /* @__PURE__ */ new Map();
  return {
    name: DRIVER_NAME$1,
    getInstance: () => data,
    hasItem(key) {
      return data.has(key);
    },
    getItem(key) {
      return data.get(key) ?? null;
    },
    getItemRaw(key) {
      return data.get(key) ?? null;
    },
    setItem(key, value) {
      data.set(key, value);
    },
    setItemRaw(key, value) {
      data.set(key, value);
    },
    removeItem(key) {
      data.delete(key);
    },
    getKeys() {
      return [...data.keys()];
    },
    clear() {
      data.clear();
    },
    dispose() {
      data.clear();
    }
  };
});

function createStorage(options = {}) {
  const context = {
    mounts: { "": options.driver || memory() },
    mountpoints: [""],
    watching: false,
    watchListeners: [],
    unwatch: {}
  };
  const getMount = (key) => {
    for (const base of context.mountpoints) {
      if (key.startsWith(base)) {
        return {
          base,
          relativeKey: key.slice(base.length),
          driver: context.mounts[base]
        };
      }
    }
    return {
      base: "",
      relativeKey: key,
      driver: context.mounts[""]
    };
  };
  const getMounts = (base, includeParent) => {
    return context.mountpoints.filter(
      (mountpoint) => mountpoint.startsWith(base) || includeParent && base.startsWith(mountpoint)
    ).map((mountpoint) => ({
      relativeBase: base.length > mountpoint.length ? base.slice(mountpoint.length) : void 0,
      mountpoint,
      driver: context.mounts[mountpoint]
    }));
  };
  const onChange = (event, key) => {
    if (!context.watching) {
      return;
    }
    key = normalizeKey$1(key);
    for (const listener of context.watchListeners) {
      listener(event, key);
    }
  };
  const startWatch = async () => {
    if (context.watching) {
      return;
    }
    context.watching = true;
    for (const mountpoint in context.mounts) {
      context.unwatch[mountpoint] = await watch(
        context.mounts[mountpoint],
        onChange,
        mountpoint
      );
    }
  };
  const stopWatch = async () => {
    if (!context.watching) {
      return;
    }
    for (const mountpoint in context.unwatch) {
      await context.unwatch[mountpoint]();
    }
    context.unwatch = {};
    context.watching = false;
  };
  const runBatch = (items, commonOptions, cb) => {
    const batches = /* @__PURE__ */ new Map();
    const getBatch = (mount) => {
      let batch = batches.get(mount.base);
      if (!batch) {
        batch = {
          driver: mount.driver,
          base: mount.base,
          items: []
        };
        batches.set(mount.base, batch);
      }
      return batch;
    };
    for (const item of items) {
      const isStringItem = typeof item === "string";
      const key = normalizeKey$1(isStringItem ? item : item.key);
      const value = isStringItem ? void 0 : item.value;
      const options2 = isStringItem || !item.options ? commonOptions : { ...commonOptions, ...item.options };
      const mount = getMount(key);
      getBatch(mount).items.push({
        key,
        value,
        relativeKey: mount.relativeKey,
        options: options2
      });
    }
    return Promise.all([...batches.values()].map((batch) => cb(batch))).then(
      (r) => r.flat()
    );
  };
  const storage = {
    // Item
    hasItem(key, opts = {}) {
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      return asyncCall(driver.hasItem, relativeKey, opts);
    },
    getItem(key, opts = {}) {
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      return asyncCall(driver.getItem, relativeKey, opts).then(
        (value) => destr(value)
      );
    },
    getItems(items, commonOptions = {}) {
      return runBatch(items, commonOptions, (batch) => {
        if (batch.driver.getItems) {
          return asyncCall(
            batch.driver.getItems,
            batch.items.map((item) => ({
              key: item.relativeKey,
              options: item.options
            })),
            commonOptions
          ).then(
            (r) => r.map((item) => ({
              key: joinKeys(batch.base, item.key),
              value: destr(item.value)
            }))
          );
        }
        return Promise.all(
          batch.items.map((item) => {
            return asyncCall(
              batch.driver.getItem,
              item.relativeKey,
              item.options
            ).then((value) => ({
              key: item.key,
              value: destr(value)
            }));
          })
        );
      });
    },
    getItemRaw(key, opts = {}) {
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      if (driver.getItemRaw) {
        return asyncCall(driver.getItemRaw, relativeKey, opts);
      }
      return asyncCall(driver.getItem, relativeKey, opts).then(
        (value) => deserializeRaw(value)
      );
    },
    async setItem(key, value, opts = {}) {
      if (value === void 0) {
        return storage.removeItem(key);
      }
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      if (!driver.setItem) {
        return;
      }
      await asyncCall(driver.setItem, relativeKey, stringify(value), opts);
      if (!driver.watch) {
        onChange("update", key);
      }
    },
    async setItems(items, commonOptions) {
      await runBatch(items, commonOptions, async (batch) => {
        if (batch.driver.setItems) {
          return asyncCall(
            batch.driver.setItems,
            batch.items.map((item) => ({
              key: item.relativeKey,
              value: stringify(item.value),
              options: item.options
            })),
            commonOptions
          );
        }
        if (!batch.driver.setItem) {
          return;
        }
        await Promise.all(
          batch.items.map((item) => {
            return asyncCall(
              batch.driver.setItem,
              item.relativeKey,
              stringify(item.value),
              item.options
            );
          })
        );
      });
    },
    async setItemRaw(key, value, opts = {}) {
      if (value === void 0) {
        return storage.removeItem(key, opts);
      }
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      if (driver.setItemRaw) {
        await asyncCall(driver.setItemRaw, relativeKey, value, opts);
      } else if (driver.setItem) {
        await asyncCall(driver.setItem, relativeKey, serializeRaw(value), opts);
      } else {
        return;
      }
      if (!driver.watch) {
        onChange("update", key);
      }
    },
    async removeItem(key, opts = {}) {
      if (typeof opts === "boolean") {
        opts = { removeMeta: opts };
      }
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      if (!driver.removeItem) {
        return;
      }
      await asyncCall(driver.removeItem, relativeKey, opts);
      if (opts.removeMeta || opts.removeMata) {
        await asyncCall(driver.removeItem, relativeKey + "$", opts);
      }
      if (!driver.watch) {
        onChange("remove", key);
      }
    },
    // Meta
    async getMeta(key, opts = {}) {
      if (typeof opts === "boolean") {
        opts = { nativeOnly: opts };
      }
      key = normalizeKey$1(key);
      const { relativeKey, driver } = getMount(key);
      const meta = /* @__PURE__ */ Object.create(null);
      if (driver.getMeta) {
        Object.assign(meta, await asyncCall(driver.getMeta, relativeKey, opts));
      }
      if (!opts.nativeOnly) {
        const value = await asyncCall(
          driver.getItem,
          relativeKey + "$",
          opts
        ).then((value_) => destr(value_));
        if (value && typeof value === "object") {
          if (typeof value.atime === "string") {
            value.atime = new Date(value.atime);
          }
          if (typeof value.mtime === "string") {
            value.mtime = new Date(value.mtime);
          }
          Object.assign(meta, value);
        }
      }
      return meta;
    },
    setMeta(key, value, opts = {}) {
      return this.setItem(key + "$", value, opts);
    },
    removeMeta(key, opts = {}) {
      return this.removeItem(key + "$", opts);
    },
    // Keys
    async getKeys(base, opts = {}) {
      base = normalizeBaseKey(base);
      const mounts = getMounts(base, true);
      let maskedMounts = [];
      const allKeys = [];
      let allMountsSupportMaxDepth = true;
      for (const mount of mounts) {
        if (!mount.driver.flags?.maxDepth) {
          allMountsSupportMaxDepth = false;
        }
        const rawKeys = await asyncCall(
          mount.driver.getKeys,
          mount.relativeBase,
          opts
        );
        for (const key of rawKeys) {
          const fullKey = mount.mountpoint + normalizeKey$1(key);
          if (!maskedMounts.some((p) => fullKey.startsWith(p))) {
            allKeys.push(fullKey);
          }
        }
        maskedMounts = [
          mount.mountpoint,
          ...maskedMounts.filter((p) => !p.startsWith(mount.mountpoint))
        ];
      }
      const shouldFilterByDepth = opts.maxDepth !== void 0 && !allMountsSupportMaxDepth;
      return allKeys.filter(
        (key) => (!shouldFilterByDepth || filterKeyByDepth(key, opts.maxDepth)) && filterKeyByBase(key, base)
      );
    },
    // Utils
    async clear(base, opts = {}) {
      base = normalizeBaseKey(base);
      await Promise.all(
        getMounts(base, false).map(async (m) => {
          if (m.driver.clear) {
            return asyncCall(m.driver.clear, m.relativeBase, opts);
          }
          if (m.driver.removeItem) {
            const keys = await m.driver.getKeys(m.relativeBase || "", opts);
            return Promise.all(
              keys.map((key) => m.driver.removeItem(key, opts))
            );
          }
        })
      );
    },
    async dispose() {
      await Promise.all(
        Object.values(context.mounts).map((driver) => dispose(driver))
      );
    },
    async watch(callback) {
      await startWatch();
      context.watchListeners.push(callback);
      return async () => {
        context.watchListeners = context.watchListeners.filter(
          (listener) => listener !== callback
        );
        if (context.watchListeners.length === 0) {
          await stopWatch();
        }
      };
    },
    async unwatch() {
      context.watchListeners = [];
      await stopWatch();
    },
    // Mount
    mount(base, driver) {
      base = normalizeBaseKey(base);
      if (base && context.mounts[base]) {
        throw new Error(`already mounted at ${base}`);
      }
      if (base) {
        context.mountpoints.push(base);
        context.mountpoints.sort((a, b) => b.length - a.length);
      }
      context.mounts[base] = driver;
      if (context.watching) {
        Promise.resolve(watch(driver, onChange, base)).then((unwatcher) => {
          context.unwatch[base] = unwatcher;
        }).catch(console.error);
      }
      return storage;
    },
    async unmount(base, _dispose = true) {
      base = normalizeBaseKey(base);
      if (!base || !context.mounts[base]) {
        return;
      }
      if (context.watching && base in context.unwatch) {
        context.unwatch[base]?.();
        delete context.unwatch[base];
      }
      if (_dispose) {
        await dispose(context.mounts[base]);
      }
      context.mountpoints = context.mountpoints.filter((key) => key !== base);
      delete context.mounts[base];
    },
    getMount(key = "") {
      key = normalizeKey$1(key) + ":";
      const m = getMount(key);
      return {
        driver: m.driver,
        base: m.base
      };
    },
    getMounts(base = "", opts = {}) {
      base = normalizeKey$1(base);
      const mounts = getMounts(base, opts.parents);
      return mounts.map((m) => ({
        driver: m.driver,
        base: m.mountpoint
      }));
    },
    // Aliases
    keys: (base, opts = {}) => storage.getKeys(base, opts),
    get: (key, opts = {}) => storage.getItem(key, opts),
    set: (key, value, opts = {}) => storage.setItem(key, value, opts),
    has: (key, opts = {}) => storage.hasItem(key, opts),
    del: (key, opts = {}) => storage.removeItem(key, opts),
    remove: (key, opts = {}) => storage.removeItem(key, opts)
  };
  return storage;
}
function watch(driver, onChange, base) {
  return driver.watch ? driver.watch((event, key) => onChange(event, base + key)) : () => {
  };
}
async function dispose(driver) {
  if (typeof driver.dispose === "function") {
    await asyncCall(driver.dispose);
  }
}

const _assets = {

};

const normalizeKey = function normalizeKey(key) {
  if (!key) {
    return "";
  }
  return key.split("?")[0]?.replace(/[/\\]/g, ":").replace(/:+/g, ":").replace(/^:|:$/g, "") || "";
};

const assets$1 = {
  getKeys() {
    return Promise.resolve(Object.keys(_assets))
  },
  hasItem (id) {
    id = normalizeKey(id);
    return Promise.resolve(id in _assets)
  },
  getItem (id) {
    id = normalizeKey(id);
    return Promise.resolve(_assets[id] ? _assets[id].import() : null)
  },
  getMeta (id) {
    id = normalizeKey(id);
    return Promise.resolve(_assets[id] ? _assets[id].meta : {})
  }
};

function defineDriver(factory) {
  return factory;
}
function createError(driver, message, opts) {
  const err = new Error(`[unstorage] [${driver}] ${message}`, opts);
  if (Error.captureStackTrace) {
    Error.captureStackTrace(err, createError);
  }
  return err;
}
function createRequiredError(driver, name) {
  if (Array.isArray(name)) {
    return createError(
      driver,
      `Missing some of the required options ${name.map((n) => "`" + n + "`").join(", ")}`
    );
  }
  return createError(driver, `Missing required option \`${name}\`.`);
}

function ignoreNotfound(err) {
  return err.code === "ENOENT" || err.code === "EISDIR" ? null : err;
}
function ignoreExists(err) {
  return err.code === "EEXIST" ? null : err;
}
async function writeFile(path, data, encoding) {
  await ensuredir(dirname$1(path));
  return promises.writeFile(path, data, encoding);
}
function readFile(path, encoding) {
  return promises.readFile(path, encoding).catch(ignoreNotfound);
}
function unlink(path) {
  return promises.unlink(path).catch(ignoreNotfound);
}
function readdir(dir) {
  return promises.readdir(dir, { withFileTypes: true }).catch(ignoreNotfound).then((r) => r || []);
}
async function ensuredir(dir) {
  if (existsSync(dir)) {
    return;
  }
  await ensuredir(dirname$1(dir)).catch(ignoreExists);
  await promises.mkdir(dir).catch(ignoreExists);
}
async function readdirRecursive(dir, ignore, maxDepth) {
  if (ignore && ignore(dir)) {
    return [];
  }
  const entries = await readdir(dir);
  const files = [];
  await Promise.all(
    entries.map(async (entry) => {
      const entryPath = resolve$1(dir, entry.name);
      if (entry.isDirectory()) {
        if (maxDepth === void 0 || maxDepth > 0) {
          const dirFiles = await readdirRecursive(
            entryPath,
            ignore,
            maxDepth === void 0 ? void 0 : maxDepth - 1
          );
          files.push(...dirFiles.map((f) => entry.name + "/" + f));
        }
      } else {
        if (!(ignore && ignore(entry.name))) {
          files.push(entry.name);
        }
      }
    })
  );
  return files;
}
async function rmRecursive(dir) {
  const entries = await readdir(dir);
  await Promise.all(
    entries.map((entry) => {
      const entryPath = resolve$1(dir, entry.name);
      if (entry.isDirectory()) {
        return rmRecursive(entryPath).then(() => promises.rmdir(entryPath));
      } else {
        return promises.unlink(entryPath);
      }
    })
  );
}

const PATH_TRAVERSE_RE = /\.\.:|\.\.$/;
const DRIVER_NAME = "fs-lite";
const unstorage_47drivers_47fs_45lite = defineDriver((opts = {}) => {
  if (!opts.base) {
    throw createRequiredError(DRIVER_NAME, "base");
  }
  opts.base = resolve$1(opts.base);
  const r = (key) => {
    if (PATH_TRAVERSE_RE.test(key)) {
      throw createError(
        DRIVER_NAME,
        `Invalid key: ${JSON.stringify(key)}. It should not contain .. segments`
      );
    }
    const resolved = join(opts.base, key.replace(/:/g, "/"));
    return resolved;
  };
  return {
    name: DRIVER_NAME,
    options: opts,
    flags: {
      maxDepth: true
    },
    hasItem(key) {
      return existsSync(r(key));
    },
    getItem(key) {
      return readFile(r(key), "utf8");
    },
    getItemRaw(key) {
      return readFile(r(key));
    },
    async getMeta(key) {
      const { atime, mtime, size, birthtime, ctime } = await promises.stat(r(key)).catch(() => ({}));
      return { atime, mtime, size, birthtime, ctime };
    },
    setItem(key, value) {
      if (opts.readOnly) {
        return;
      }
      return writeFile(r(key), value, "utf8");
    },
    setItemRaw(key, value) {
      if (opts.readOnly) {
        return;
      }
      return writeFile(r(key), value);
    },
    removeItem(key) {
      if (opts.readOnly) {
        return;
      }
      return unlink(r(key));
    },
    getKeys(_base, topts) {
      return readdirRecursive(r("."), opts.ignore, topts?.maxDepth);
    },
    async clear() {
      if (opts.readOnly || opts.noClear) {
        return;
      }
      await rmRecursive(r("."));
    }
  };
});

const storage = createStorage({});

storage.mount('/assets', assets$1);

storage.mount('data', unstorage_47drivers_47fs_45lite({"driver":"fsLite","base":"./.data/kv"}));

function useStorage(base = "") {
  return base ? prefixStorage(storage, base) : storage;
}

const e=globalThis.process?.getBuiltinModule?.("crypto")?.hash,r="sha256",s="base64url";function digest(t){if(e)return e(r,t,s);const o=createHash(r).update(t);return globalThis.process?.versions?.webcontainer?o.digest().toString(s):o.digest(s)}

const Hasher = /* @__PURE__ */ (() => {
  class Hasher2 {
    buff = "";
    #context = /* @__PURE__ */ new Map();
    write(str) {
      this.buff += str;
    }
    dispatch(value) {
      const type = value === null ? "null" : typeof value;
      return this[type](value);
    }
    object(object) {
      if (object && typeof object.toJSON === "function") {
        return this.object(object.toJSON());
      }
      const objString = Object.prototype.toString.call(object);
      let objType = "";
      const objectLength = objString.length;
      objType = objectLength < 10 ? "unknown:[" + objString + "]" : objString.slice(8, objectLength - 1);
      objType = objType.toLowerCase();
      let objectNumber = null;
      if ((objectNumber = this.#context.get(object)) === void 0) {
        this.#context.set(object, this.#context.size);
      } else {
        return this.dispatch("[CIRCULAR:" + objectNumber + "]");
      }
      if (typeof Buffer !== "undefined" && Buffer.isBuffer && Buffer.isBuffer(object)) {
        this.write("buffer:");
        return this.write(object.toString("utf8"));
      }
      if (objType !== "object" && objType !== "function" && objType !== "asyncfunction") {
        if (this[objType]) {
          this[objType](object);
        } else {
          this.unknown(object, objType);
        }
      } else {
        const keys = Object.keys(object).sort();
        const extraKeys = [];
        this.write("object:" + (keys.length + extraKeys.length) + ":");
        const dispatchForKey = (key) => {
          this.dispatch(key);
          this.write(":");
          this.dispatch(object[key]);
          this.write(",");
        };
        for (const key of keys) {
          dispatchForKey(key);
        }
        for (const key of extraKeys) {
          dispatchForKey(key);
        }
      }
    }
    array(arr, unordered) {
      unordered = unordered === void 0 ? false : unordered;
      this.write("array:" + arr.length + ":");
      if (!unordered || arr.length <= 1) {
        for (const entry of arr) {
          this.dispatch(entry);
        }
        return;
      }
      const contextAdditions = /* @__PURE__ */ new Map();
      const entries = arr.map((entry) => {
        const hasher = new Hasher2();
        hasher.dispatch(entry);
        for (const [key, value] of hasher.#context) {
          contextAdditions.set(key, value);
        }
        return hasher.toString();
      });
      this.#context = contextAdditions;
      entries.sort();
      return this.array(entries, false);
    }
    date(date) {
      return this.write("date:" + date.toJSON());
    }
    symbol(sym) {
      return this.write("symbol:" + sym.toString());
    }
    unknown(value, type) {
      this.write(type);
      if (!value) {
        return;
      }
      this.write(":");
      if (value && typeof value.entries === "function") {
        return this.array(
          [...value.entries()],
          true
          /* ordered */
        );
      }
    }
    error(err) {
      return this.write("error:" + err.toString());
    }
    boolean(bool) {
      return this.write("bool:" + bool);
    }
    string(string) {
      this.write("string:" + string.length + ":");
      this.write(string);
    }
    function(fn) {
      this.write("fn:");
      if (isNativeFunction(fn)) {
        this.dispatch("[native]");
      } else {
        this.dispatch(fn.toString());
      }
    }
    number(number) {
      return this.write("number:" + number);
    }
    null() {
      return this.write("Null");
    }
    undefined() {
      return this.write("Undefined");
    }
    regexp(regex) {
      return this.write("regex:" + regex.toString());
    }
    arraybuffer(arr) {
      this.write("arraybuffer:");
      return this.dispatch(new Uint8Array(arr));
    }
    url(url) {
      return this.write("url:" + url.toString());
    }
    map(map) {
      this.write("map:");
      const arr = [...map];
      return this.array(arr, false);
    }
    set(set) {
      this.write("set:");
      const arr = [...set];
      return this.array(arr, false);
    }
    bigint(number) {
      return this.write("bigint:" + number.toString());
    }
  }
  for (const type of [
    "uint8array",
    "uint8clampedarray",
    "unt8array",
    "uint16array",
    "unt16array",
    "uint32array",
    "unt32array",
    "float32array",
    "float64array"
  ]) {
    Hasher2.prototype[type] = function(arr) {
      this.write(type + ":");
      return this.array([...arr], false);
    };
  }
  function isNativeFunction(f) {
    if (typeof f !== "function") {
      return false;
    }
    return Function.prototype.toString.call(f).slice(
      -15
      /* "[native code] }".length */
    ) === "[native code] }";
  }
  return Hasher2;
})();
function serialize(object) {
  const hasher = new Hasher();
  hasher.dispatch(object);
  return hasher.buff;
}
function hash(value) {
  return digest(typeof value === "string" ? value : serialize(value)).replace(/[-_]/g, "").slice(0, 10);
}

function defaultCacheOptions() {
  return {
    name: "_",
    base: "/cache",
    swr: true,
    maxAge: 1
  };
}
function defineCachedFunction(fn, opts = {}) {
  opts = { ...defaultCacheOptions(), ...opts };
  const pending = {};
  const group = opts.group || "nitro/functions";
  const name = opts.name || fn.name || "_";
  const integrity = opts.integrity || hash([fn, opts]);
  const validate = opts.validate || ((entry) => entry.value !== void 0);
  async function get(key, resolver, shouldInvalidateCache, event) {
    const cacheKey = [opts.base, group, name, key + ".json"].filter(Boolean).join(":").replace(/:\/$/, ":index");
    let entry = await useStorage().getItem(cacheKey).catch((error) => {
      console.error(`[cache] Cache read error.`, error);
      useNitroApp().captureError(error, { event, tags: ["cache"] });
    }) || {};
    if (typeof entry !== "object") {
      entry = {};
      const error = new Error("Malformed data read from cache.");
      console.error("[cache]", error);
      useNitroApp().captureError(error, { event, tags: ["cache"] });
    }
    const ttl = (opts.maxAge ?? 0) * 1e3;
    if (ttl) {
      entry.expires = Date.now() + ttl;
    }
    const expired = shouldInvalidateCache || entry.integrity !== integrity || ttl && Date.now() - (entry.mtime || 0) > ttl || validate(entry) === false;
    const _resolve = async () => {
      const isPending = pending[key];
      if (!isPending) {
        if (entry.value !== void 0 && (opts.staleMaxAge || 0) >= 0 && opts.swr === false) {
          entry.value = void 0;
          entry.integrity = void 0;
          entry.mtime = void 0;
          entry.expires = void 0;
        }
        pending[key] = Promise.resolve(resolver());
      }
      try {
        entry.value = await pending[key];
      } catch (error) {
        if (!isPending) {
          delete pending[key];
        }
        throw error;
      }
      if (!isPending) {
        entry.mtime = Date.now();
        entry.integrity = integrity;
        delete pending[key];
        if (validate(entry) !== false) {
          let setOpts;
          if (opts.maxAge && !opts.swr) {
            setOpts = { ttl: opts.maxAge };
          }
          const promise = useStorage().setItem(cacheKey, entry, setOpts).catch((error) => {
            console.error(`[cache] Cache write error.`, error);
            useNitroApp().captureError(error, { event, tags: ["cache"] });
          });
          if (event?.waitUntil) {
            event.waitUntil(promise);
          }
        }
      }
    };
    const _resolvePromise = expired ? _resolve() : Promise.resolve();
    if (entry.value === void 0) {
      await _resolvePromise;
    } else if (expired && event && event.waitUntil) {
      event.waitUntil(_resolvePromise);
    }
    if (opts.swr && validate(entry) !== false) {
      _resolvePromise.catch((error) => {
        console.error(`[cache] SWR handler error.`, error);
        useNitroApp().captureError(error, { event, tags: ["cache"] });
      });
      return entry;
    }
    return _resolvePromise.then(() => entry);
  }
  return async (...args) => {
    const shouldBypassCache = await opts.shouldBypassCache?.(...args);
    if (shouldBypassCache) {
      return fn(...args);
    }
    const key = await (opts.getKey || getKey)(...args);
    const shouldInvalidateCache = await opts.shouldInvalidateCache?.(...args);
    const entry = await get(
      key,
      () => fn(...args),
      shouldInvalidateCache,
      args[0] && isEvent(args[0]) ? args[0] : void 0
    );
    let value = entry.value;
    if (opts.transform) {
      value = await opts.transform(entry, ...args) || value;
    }
    return value;
  };
}
function cachedFunction(fn, opts = {}) {
  return defineCachedFunction(fn, opts);
}
function getKey(...args) {
  return args.length > 0 ? hash(args) : "";
}
function escapeKey(key) {
  return String(key).replace(/\W/g, "");
}
function defineCachedEventHandler(handler, opts = defaultCacheOptions()) {
  const variableHeaderNames = (opts.varies || []).filter(Boolean).map((h) => h.toLowerCase()).sort();
  const _opts = {
    ...opts,
    getKey: async (event) => {
      const customKey = await opts.getKey?.(event);
      if (customKey) {
        return escapeKey(customKey);
      }
      const _path = event.node.req.originalUrl || event.node.req.url || event.path;
      let _pathname;
      try {
        _pathname = escapeKey(decodeURI(parseURL(_path).pathname)).slice(0, 16) || "index";
      } catch {
        _pathname = "-";
      }
      const _hashedPath = `${_pathname}.${hash(_path)}`;
      const _headers = variableHeaderNames.map((header) => [header, event.node.req.headers[header]]).map(([name, value]) => `${escapeKey(name)}.${hash(value)}`);
      return [_hashedPath, ..._headers].join(":");
    },
    validate: (entry) => {
      if (!entry.value) {
        return false;
      }
      if (entry.value.code >= 400) {
        return false;
      }
      if (entry.value.body === void 0) {
        return false;
      }
      if (entry.value.headers.etag === "undefined" || entry.value.headers["last-modified"] === "undefined") {
        return false;
      }
      return true;
    },
    group: opts.group || "nitro/handlers",
    integrity: opts.integrity || hash([handler, opts])
  };
  const _cachedHandler = cachedFunction(
    async (incomingEvent) => {
      const variableHeaders = {};
      for (const header of variableHeaderNames) {
        const value = incomingEvent.node.req.headers[header];
        if (value !== void 0) {
          variableHeaders[header] = value;
        }
      }
      const reqProxy = cloneWithProxy(incomingEvent.node.req, {
        headers: variableHeaders
      });
      const resHeaders = {};
      let _resSendBody;
      const resProxy = cloneWithProxy(incomingEvent.node.res, {
        statusCode: 200,
        writableEnded: false,
        writableFinished: false,
        headersSent: false,
        closed: false,
        getHeader(name) {
          return resHeaders[name];
        },
        setHeader(name, value) {
          resHeaders[name] = value;
          return this;
        },
        getHeaderNames() {
          return Object.keys(resHeaders);
        },
        hasHeader(name) {
          return name in resHeaders;
        },
        removeHeader(name) {
          delete resHeaders[name];
        },
        getHeaders() {
          return resHeaders;
        },
        end(chunk, arg2, arg3) {
          if (typeof chunk === "string") {
            _resSendBody = chunk;
          }
          if (typeof arg2 === "function") {
            arg2();
          }
          if (typeof arg3 === "function") {
            arg3();
          }
          return this;
        },
        write(chunk, arg2, arg3) {
          if (typeof chunk === "string") {
            _resSendBody = chunk;
          }
          if (typeof arg2 === "function") {
            arg2(void 0);
          }
          if (typeof arg3 === "function") {
            arg3();
          }
          return true;
        },
        writeHead(statusCode, headers2) {
          this.statusCode = statusCode;
          if (headers2) {
            if (Array.isArray(headers2) || typeof headers2 === "string") {
              throw new TypeError("Raw headers  is not supported.");
            }
            for (const header in headers2) {
              const value = headers2[header];
              if (value !== void 0) {
                this.setHeader(
                  header,
                  value
                );
              }
            }
          }
          return this;
        }
      });
      const event = createEvent(reqProxy, resProxy);
      event.fetch = (url, fetchOptions) => fetchWithEvent(event, url, fetchOptions, {
        fetch: useNitroApp().localFetch
      });
      event.$fetch = (url, fetchOptions) => fetchWithEvent(event, url, fetchOptions, {
        fetch: globalThis.$fetch
      });
      event.waitUntil = incomingEvent.waitUntil;
      event.context = incomingEvent.context;
      event.context.cache = {
        options: _opts
      };
      const body = await handler(event) || _resSendBody;
      const headers = event.node.res.getHeaders();
      headers.etag = String(
        headers.Etag || headers.etag || `W/"${hash(body)}"`
      );
      headers["last-modified"] = String(
        headers["Last-Modified"] || headers["last-modified"] || (/* @__PURE__ */ new Date()).toUTCString()
      );
      const cacheControl = [];
      if (opts.swr) {
        if (opts.maxAge) {
          cacheControl.push(`s-maxage=${opts.maxAge}`);
        }
        if (opts.staleMaxAge) {
          cacheControl.push(`stale-while-revalidate=${opts.staleMaxAge}`);
        } else {
          cacheControl.push("stale-while-revalidate");
        }
      } else if (opts.maxAge) {
        cacheControl.push(`max-age=${opts.maxAge}`);
      }
      if (cacheControl.length > 0) {
        headers["cache-control"] = cacheControl.join(", ");
      }
      const cacheEntry = {
        code: event.node.res.statusCode,
        headers,
        body
      };
      return cacheEntry;
    },
    _opts
  );
  return defineEventHandler(async (event) => {
    if (opts.headersOnly) {
      if (handleCacheHeaders(event, { maxAge: opts.maxAge })) {
        return;
      }
      return handler(event);
    }
    const response = await _cachedHandler(
      event
    );
    if (event.node.res.headersSent || event.node.res.writableEnded) {
      return response.body;
    }
    if (handleCacheHeaders(event, {
      modifiedTime: new Date(response.headers["last-modified"]),
      etag: response.headers.etag,
      maxAge: opts.maxAge
    })) {
      return;
    }
    event.node.res.statusCode = response.code;
    for (const name in response.headers) {
      const value = response.headers[name];
      if (name === "set-cookie") {
        event.node.res.appendHeader(
          name,
          splitCookiesString(value)
        );
      } else {
        if (value !== void 0) {
          event.node.res.setHeader(name, value);
        }
      }
    }
    return response.body;
  });
}
function cloneWithProxy(obj, overrides) {
  return new Proxy(obj, {
    get(target, property, receiver) {
      if (property in overrides) {
        return overrides[property];
      }
      return Reflect.get(target, property, receiver);
    },
    set(target, property, value, receiver) {
      if (property in overrides) {
        overrides[property] = value;
        return true;
      }
      return Reflect.set(target, property, value, receiver);
    }
  });
}
const cachedEventHandler = defineCachedEventHandler;

function klona(x) {
	if (typeof x !== 'object') return x;

	var k, tmp, str=Object.prototype.toString.call(x);

	if (str === '[object Object]') {
		if (x.constructor !== Object && typeof x.constructor === 'function') {
			tmp = new x.constructor();
			for (k in x) {
				if (x.hasOwnProperty(k) && tmp[k] !== x[k]) {
					tmp[k] = klona(x[k]);
				}
			}
		} else {
			tmp = {}; // null
			for (k in x) {
				if (k === '__proto__') {
					Object.defineProperty(tmp, k, {
						value: klona(x[k]),
						configurable: true,
						enumerable: true,
						writable: true,
					});
				} else {
					tmp[k] = klona(x[k]);
				}
			}
		}
		return tmp;
	}

	if (str === '[object Array]') {
		k = x.length;
		for (tmp=Array(k); k--;) {
			tmp[k] = klona(x[k]);
		}
		return tmp;
	}

	if (str === '[object Set]') {
		tmp = new Set;
		x.forEach(function (val) {
			tmp.add(klona(val));
		});
		return tmp;
	}

	if (str === '[object Map]') {
		tmp = new Map;
		x.forEach(function (val, key) {
			tmp.set(klona(key), klona(val));
		});
		return tmp;
	}

	if (str === '[object Date]') {
		return new Date(+x);
	}

	if (str === '[object RegExp]') {
		tmp = new RegExp(x.source, x.flags);
		tmp.lastIndex = x.lastIndex;
		return tmp;
	}

	if (str === '[object DataView]') {
		return new x.constructor( klona(x.buffer) );
	}

	if (str === '[object ArrayBuffer]') {
		return x.slice(0);
	}

	// ArrayBuffer.isView(x)
	// ~> `new` bcuz `Buffer.slice` => ref
	if (str.slice(-6) === 'Array]') {
		return new x.constructor(x);
	}

	return x;
}

const inlineAppConfig = {
  "nuxt": {}
};



const appConfig = defuFn(inlineAppConfig);

const NUMBER_CHAR_RE = /\d/;
const STR_SPLITTERS = ["-", "_", "/", "."];
function isUppercase(char = "") {
  if (NUMBER_CHAR_RE.test(char)) {
    return void 0;
  }
  return char !== char.toLowerCase();
}
function splitByCase(str, separators) {
  const splitters = STR_SPLITTERS;
  const parts = [];
  if (!str || typeof str !== "string") {
    return parts;
  }
  let buff = "";
  let previousUpper;
  let previousSplitter;
  for (const char of str) {
    const isSplitter = splitters.includes(char);
    if (isSplitter === true) {
      parts.push(buff);
      buff = "";
      previousUpper = void 0;
      continue;
    }
    const isUpper = isUppercase(char);
    if (previousSplitter === false) {
      if (previousUpper === false && isUpper === true) {
        parts.push(buff);
        buff = char;
        previousUpper = isUpper;
        continue;
      }
      if (previousUpper === true && isUpper === false && buff.length > 1) {
        const lastChar = buff.at(-1);
        parts.push(buff.slice(0, Math.max(0, buff.length - 1)));
        buff = lastChar + char;
        previousUpper = isUpper;
        continue;
      }
    }
    buff += char;
    previousUpper = isUpper;
    previousSplitter = isSplitter;
  }
  parts.push(buff);
  return parts;
}
function kebabCase(str, joiner) {
  return str ? (Array.isArray(str) ? str : splitByCase(str)).map((p) => p.toLowerCase()).join(joiner) : "";
}
function snakeCase(str) {
  return kebabCase(str || "", "_");
}

function getEnv(key, opts) {
  const envKey = snakeCase(key).toUpperCase();
  return destr(
    process.env[opts.prefix + envKey] ?? process.env[opts.altPrefix + envKey]
  );
}
function _isObject(input) {
  return typeof input === "object" && !Array.isArray(input);
}
function applyEnv(obj, opts, parentKey = "") {
  for (const key in obj) {
    const subKey = parentKey ? `${parentKey}_${key}` : key;
    const envValue = getEnv(subKey, opts);
    if (_isObject(obj[key])) {
      if (_isObject(envValue)) {
        obj[key] = { ...obj[key], ...envValue };
        applyEnv(obj[key], opts, subKey);
      } else if (envValue === void 0) {
        applyEnv(obj[key], opts, subKey);
      } else {
        obj[key] = envValue ?? obj[key];
      }
    } else {
      obj[key] = envValue ?? obj[key];
    }
    if (opts.envExpansion && typeof obj[key] === "string") {
      obj[key] = _expandFromEnv(obj[key]);
    }
  }
  return obj;
}
const envExpandRx = /\{\{([^{}]*)\}\}/g;
function _expandFromEnv(value) {
  return value.replace(envExpandRx, (match, key) => {
    return process.env[key] || match;
  });
}

const _inlineRuntimeConfig = {
  "app": {
    "baseURL": "",
    "buildId": "3c9b37e7-ce63-4c35-bd26-1de57f5b352e",
    "buildAssetsDir": "/_nuxt/",
    "cdnURL": ""
  },
  "nitro": {
    "envPrefix": "NUXT_",
    "routeRules": {
      "/__nuxt_error": {
        "cache": false
      },
      "/_nuxt/builds/meta/**": {
        "headers": {
          "cache-control": "public, max-age=31536000, immutable"
        }
      },
      "/_nuxt/builds/**": {
        "headers": {
          "cache-control": "public, max-age=1, immutable"
        }
      },
      "/_fonts/**": {
        "headers": {
          "cache-control": "public, max-age=31536000, immutable"
        }
      },
      "/_nuxt/**": {
        "headers": {
          "cache-control": "public, max-age=31536000, immutable"
        }
      }
    }
  },
  "public": {
    "AUTH_TOKEN": "mealie.access_token",
    "GLOBAL_MIDDLEWARE": "",
    "SUB_PATH": "",
    "useDark": false,
    "themes": {
      "dark": {
        "primary": "#E58325",
        "accent": "#007A99",
        "secondary": "#973542",
        "success": "#43A047",
        "info": "#1976d2",
        "warning": "#FF6D00",
        "error": "#EF5350",
        "background": "#1E1E1E"
      },
      "light": {
        "primary": "#E58325",
        "accent": "#007A99",
        "secondary": "#973542",
        "success": "#43A047",
        "info": "#1976d2",
        "warning": "#FF6D00",
        "error": "#EF5350"
      }
    },
    "i18n": {
      "baseUrl": "",
      "defaultLocale": "en-US",
      "defaultDirection": "ltr",
      "strategy": "no_prefix",
      "lazy": true,
      "rootRedirect": "",
      "routesNameSeparator": "___",
      "defaultLocaleRouteNameSuffix": "default",
      "skipSettingLocaleOnNavigate": false,
      "differentDomains": false,
      "trailingSlash": false,
      "locales": [
        {
          "code": "af-ZA",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/af-ZA.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "ar-SA",
          "dir": "rtl",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/ar-SA.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "bg-BG",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/bg-BG.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "ca-ES",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/ca-ES.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "cs-CZ",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/cs-CZ.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "da-DK",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/da-DK.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "de-DE",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/de-DE.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "el-GR",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/el-GR.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "en-GB",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/en-GB.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "en-US",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/en-US.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "es-ES",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/es-ES.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "et-EE",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/et-EE.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "fi-FI",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/fi-FI.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "fr-BE",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/fr-BE.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "fr-CA",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/fr-CA.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "fr-FR",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/fr-FR.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "gl-ES",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/gl-ES.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "he-IL",
          "dir": "rtl",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/he-IL.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "hr-HR",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/hr-HR.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "hu-HU",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/hu-HU.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "is-IS",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/is-IS.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "it-IT",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/it-IT.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "ja-JP",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/ja-JP.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "ko-KR",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/ko-KR.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "lt-LT",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/lt-LT.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "lv-LV",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/lv-LV.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "nl-NL",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/nl-NL.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "no-NO",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/no-NO.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "pl-PL",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/pl-PL.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "pt-BR",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/pt-BR.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "pt-PT",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/pt-PT.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "ro-RO",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/ro-RO.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "ru-RU",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/ru-RU.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "sk-SK",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/sk-SK.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "sl-SI",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/sl-SI.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "sr-SP",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/sr-SP.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "sv-SE",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/sv-SE.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "tr-TR",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/tr-TR.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "uk-UA",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/uk-UA.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "vi-VN",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/vi-VN.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "zh-CN",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/zh-CN.ts",
              "cache": ""
            }
          ]
        },
        {
          "code": "zh-TW",
          "dir": "ltr",
          "files": [
            {
              "path": "/workspaces/modular-monolith-2/apps/productivity/mealie-service/apps/mealie-web/lang/locales/zh-TW.ts",
              "cache": ""
            }
          ]
        }
      ],
      "detectBrowserLanguage": {
        "alwaysRedirect": true,
        "cookieCrossOrigin": false,
        "cookieDomain": "",
        "cookieKey": "i18n_redirected",
        "cookieSecure": false,
        "fallbackLocale": "en-US",
        "redirectOn": "root",
        "useCookie": true
      },
      "experimental": {
        "localeDetector": "",
        "switchLocalePathLinkSSR": false,
        "autoImportTranslationFunctions": false,
        "typedPages": true,
        "typedOptionsAndMessages": false,
        "generatedLocaleFilePathFormat": "absolute",
        "alternateLinkCanonicalQueries": false,
        "hmr": true
      },
      "multiDomainLocales": false,
      "domainLocales": {
        "af-ZA": {
          "domain": ""
        },
        "ar-SA": {
          "domain": ""
        },
        "bg-BG": {
          "domain": ""
        },
        "ca-ES": {
          "domain": ""
        },
        "cs-CZ": {
          "domain": ""
        },
        "da-DK": {
          "domain": ""
        },
        "de-DE": {
          "domain": ""
        },
        "el-GR": {
          "domain": ""
        },
        "en-GB": {
          "domain": ""
        },
        "en-US": {
          "domain": ""
        },
        "es-ES": {
          "domain": ""
        },
        "et-EE": {
          "domain": ""
        },
        "fi-FI": {
          "domain": ""
        },
        "fr-BE": {
          "domain": ""
        },
        "fr-CA": {
          "domain": ""
        },
        "fr-FR": {
          "domain": ""
        },
        "gl-ES": {
          "domain": ""
        },
        "he-IL": {
          "domain": ""
        },
        "hr-HR": {
          "domain": ""
        },
        "hu-HU": {
          "domain": ""
        },
        "is-IS": {
          "domain": ""
        },
        "it-IT": {
          "domain": ""
        },
        "ja-JP": {
          "domain": ""
        },
        "ko-KR": {
          "domain": ""
        },
        "lt-LT": {
          "domain": ""
        },
        "lv-LV": {
          "domain": ""
        },
        "nl-NL": {
          "domain": ""
        },
        "no-NO": {
          "domain": ""
        },
        "pl-PL": {
          "domain": ""
        },
        "pt-BR": {
          "domain": ""
        },
        "pt-PT": {
          "domain": ""
        },
        "ro-RO": {
          "domain": ""
        },
        "ru-RU": {
          "domain": ""
        },
        "sk-SK": {
          "domain": ""
        },
        "sl-SI": {
          "domain": ""
        },
        "sr-SP": {
          "domain": ""
        },
        "sv-SE": {
          "domain": ""
        },
        "tr-TR": {
          "domain": ""
        },
        "uk-UA": {
          "domain": ""
        },
        "vi-VN": {
          "domain": ""
        },
        "zh-CN": {
          "domain": ""
        },
        "zh-TW": {
          "domain": ""
        }
      }
    }
  },
  "sessionPassword": "password-with-at-least-32-characters",
  "apiUrl": "http://localhost:9000"
};
const envOptions = {
  prefix: "NITRO_",
  altPrefix: _inlineRuntimeConfig.nitro.envPrefix ?? process.env.NITRO_ENV_PREFIX ?? "_",
  envExpansion: _inlineRuntimeConfig.nitro.envExpansion ?? process.env.NITRO_ENV_EXPANSION ?? false
};
const _sharedRuntimeConfig = _deepFreeze(
  applyEnv(klona(_inlineRuntimeConfig), envOptions)
);
function useRuntimeConfig(event) {
  if (!event) {
    return _sharedRuntimeConfig;
  }
  if (event.context.nitro.runtimeConfig) {
    return event.context.nitro.runtimeConfig;
  }
  const runtimeConfig = klona(_inlineRuntimeConfig);
  applyEnv(runtimeConfig, envOptions);
  event.context.nitro.runtimeConfig = runtimeConfig;
  return runtimeConfig;
}
_deepFreeze(klona(appConfig));
function _deepFreeze(object) {
  const propNames = Object.getOwnPropertyNames(object);
  for (const name of propNames) {
    const value = object[name];
    if (value && typeof value === "object") {
      _deepFreeze(value);
    }
  }
  return Object.freeze(object);
}
new Proxy(/* @__PURE__ */ Object.create(null), {
  get: (_, prop) => {
    console.warn(
      "Please use `useRuntimeConfig()` instead of accessing config directly."
    );
    const runtimeConfig = useRuntimeConfig();
    if (prop in runtimeConfig) {
      return runtimeConfig[prop];
    }
    return void 0;
  }
});

function createContext(opts = {}) {
  let currentInstance;
  let isSingleton = false;
  const checkConflict = (instance) => {
    if (currentInstance && currentInstance !== instance) {
      throw new Error("Context conflict");
    }
  };
  let als;
  if (opts.asyncContext) {
    const _AsyncLocalStorage = opts.AsyncLocalStorage || globalThis.AsyncLocalStorage;
    if (_AsyncLocalStorage) {
      als = new _AsyncLocalStorage();
    } else {
      console.warn("[unctx] `AsyncLocalStorage` is not provided.");
    }
  }
  const _getCurrentInstance = () => {
    if (als) {
      const instance = als.getStore();
      if (instance !== void 0) {
        return instance;
      }
    }
    return currentInstance;
  };
  return {
    use: () => {
      const _instance = _getCurrentInstance();
      if (_instance === void 0) {
        throw new Error("Context is not available");
      }
      return _instance;
    },
    tryUse: () => {
      return _getCurrentInstance();
    },
    set: (instance, replace) => {
      if (!replace) {
        checkConflict(instance);
      }
      currentInstance = instance;
      isSingleton = true;
    },
    unset: () => {
      currentInstance = void 0;
      isSingleton = false;
    },
    call: (instance, callback) => {
      checkConflict(instance);
      currentInstance = instance;
      try {
        return als ? als.run(instance, callback) : callback();
      } finally {
        if (!isSingleton) {
          currentInstance = void 0;
        }
      }
    },
    async callAsync(instance, callback) {
      currentInstance = instance;
      const onRestore = () => {
        currentInstance = instance;
      };
      const onLeave = () => currentInstance === instance ? onRestore : void 0;
      asyncHandlers.add(onLeave);
      try {
        const r = als ? als.run(instance, callback) : callback();
        if (!isSingleton) {
          currentInstance = void 0;
        }
        return await r;
      } finally {
        asyncHandlers.delete(onLeave);
      }
    }
  };
}
function createNamespace(defaultOpts = {}) {
  const contexts = {};
  return {
    get(key, opts = {}) {
      if (!contexts[key]) {
        contexts[key] = createContext({ ...defaultOpts, ...opts });
      }
      return contexts[key];
    }
  };
}
const _globalThis = typeof globalThis !== "undefined" ? globalThis : typeof self !== "undefined" ? self : typeof global !== "undefined" ? global : {};
const globalKey = "__unctx__";
const defaultNamespace = _globalThis[globalKey] || (_globalThis[globalKey] = createNamespace());
const getContext = (key, opts = {}) => defaultNamespace.get(key, opts);
const asyncHandlersKey = "__unctx_async_handlers__";
const asyncHandlers = _globalThis[asyncHandlersKey] || (_globalThis[asyncHandlersKey] = /* @__PURE__ */ new Set());

getContext("nitro-app", {
  asyncContext: false,
  AsyncLocalStorage: void 0
});

const config = useRuntimeConfig();
const _routeRulesMatcher = toRouteMatcher(
  createRouter$1({ routes: config.nitro.routeRules })
);
function createRouteRulesHandler(ctx) {
  return eventHandler((event) => {
    const routeRules = getRouteRules(event);
    if (routeRules.headers) {
      setHeaders(event, routeRules.headers);
    }
    if (routeRules.redirect) {
      let target = routeRules.redirect.to;
      if (target.endsWith("/**")) {
        let targetPath = event.path;
        const strpBase = routeRules.redirect._redirectStripBase;
        if (strpBase) {
          targetPath = withoutBase(targetPath, strpBase);
        }
        target = joinURL(target.slice(0, -3), targetPath);
      } else if (event.path.includes("?")) {
        const query = getQuery$1(event.path);
        target = withQuery(target, query);
      }
      return sendRedirect(event, target, routeRules.redirect.statusCode);
    }
    if (routeRules.proxy) {
      let target = routeRules.proxy.to;
      if (target.endsWith("/**")) {
        let targetPath = event.path;
        const strpBase = routeRules.proxy._proxyStripBase;
        if (strpBase) {
          targetPath = withoutBase(targetPath, strpBase);
        }
        target = joinURL(target.slice(0, -3), targetPath);
      } else if (event.path.includes("?")) {
        const query = getQuery$1(event.path);
        target = withQuery(target, query);
      }
      return proxyRequest(event, target, {
        fetch: ctx.localFetch,
        ...routeRules.proxy
      });
    }
  });
}
function getRouteRules(event) {
  event.context._nitro = event.context._nitro || {};
  if (!event.context._nitro.routeRules) {
    event.context._nitro.routeRules = getRouteRulesForPath(
      withoutBase(event.path.split("?")[0], useRuntimeConfig().app.baseURL)
    );
  }
  return event.context._nitro.routeRules;
}
function getRouteRulesForPath(path) {
  return defu({}, ..._routeRulesMatcher.matchAll(path).reverse());
}

function _captureError(error, type) {
  console.error(`[${type}]`, error);
  useNitroApp().captureError(error, { tags: [type] });
}
function trapUnhandledNodeErrors() {
  process.on(
    "unhandledRejection",
    (error) => _captureError(error, "unhandledRejection")
  );
  process.on(
    "uncaughtException",
    (error) => _captureError(error, "uncaughtException")
  );
}
function joinHeaders(value) {
  return Array.isArray(value) ? value.join(", ") : String(value);
}
function normalizeFetchResponse(response) {
  if (!response.headers.has("set-cookie")) {
    return response;
  }
  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: normalizeCookieHeaders(response.headers)
  });
}
function normalizeCookieHeader(header = "") {
  return splitCookiesString(joinHeaders(header));
}
function normalizeCookieHeaders(headers) {
  const outgoingHeaders = new Headers();
  for (const [name, header] of headers) {
    if (name === "set-cookie") {
      for (const cookie of normalizeCookieHeader(header)) {
        outgoingHeaders.append("set-cookie", cookie);
      }
    } else {
      outgoingHeaders.set(name, joinHeaders(header));
    }
  }
  return outgoingHeaders;
}

function isJsonRequest(event) {
  if (hasReqHeader(event, "accept", "text/html")) {
    return false;
  }
  return hasReqHeader(event, "accept", "application/json") || hasReqHeader(event, "user-agent", "curl/") || hasReqHeader(event, "user-agent", "httpie/") || hasReqHeader(event, "sec-fetch-mode", "cors") || event.path.startsWith("/api/") || event.path.endsWith(".json");
}
function hasReqHeader(event, name, includes) {
  const value = getRequestHeader(event, name);
  return value && typeof value === "string" && value.toLowerCase().includes(includes);
}

const errorHandler$0 = (async function errorhandler(error, event, { defaultHandler }) {
  if (event.handled || isJsonRequest(event)) {
    return;
  }
  const defaultRes = await defaultHandler(error, event, { json: true });
  const statusCode = error.statusCode || 500;
  if (statusCode === 404 && defaultRes.status === 302) {
    setResponseHeaders(event, defaultRes.headers);
    setResponseStatus(event, defaultRes.status, defaultRes.statusText);
    return send(event, JSON.stringify(defaultRes.body, null, 2));
  }
  const errorObject = defaultRes.body;
  const url = new URL(errorObject.url);
  errorObject.url = withoutBase(url.pathname, useRuntimeConfig(event).app.baseURL) + url.search + url.hash;
  errorObject.message ||= "Server Error";
  errorObject.data ||= error.data;
  errorObject.statusMessage ||= error.statusMessage;
  delete defaultRes.headers["content-type"];
  delete defaultRes.headers["content-security-policy"];
  setResponseHeaders(event, defaultRes.headers);
  const reqHeaders = getRequestHeaders(event);
  const isRenderingError = event.path.startsWith("/__nuxt_error") || !!reqHeaders["x-nuxt-error"];
  const res = isRenderingError ? null : await useNitroApp().localFetch(
    withQuery(joinURL(useRuntimeConfig(event).app.baseURL, "/__nuxt_error"), errorObject),
    {
      headers: { ...reqHeaders, "x-nuxt-error": "true" },
      redirect: "manual"
    }
  ).catch(() => null);
  if (event.handled) {
    return;
  }
  if (!res) {
    const { template } = await import('../_/error-500.mjs');
    setResponseHeader(event, "Content-Type", "text/html;charset=UTF-8");
    return send(event, template(errorObject));
  }
  const html = await res.text();
  for (const [header, value] of res.headers.entries()) {
    if (header === "set-cookie") {
      appendResponseHeader(event, header, value);
      continue;
    }
    setResponseHeader(event, header, value);
  }
  setResponseStatus(event, res.status && res.status !== 200 ? res.status : defaultRes.status, res.statusText || defaultRes.statusText);
  return send(event, html);
});

function defineNitroErrorHandler(handler) {
  return handler;
}

const errorHandler$1 = defineNitroErrorHandler(
  function defaultNitroErrorHandler(error, event) {
    const res = defaultHandler(error, event);
    setResponseHeaders(event, res.headers);
    setResponseStatus(event, res.status, res.statusText);
    return send(event, JSON.stringify(res.body, null, 2));
  }
);
function defaultHandler(error, event, opts) {
  const isSensitive = error.unhandled || error.fatal;
  const statusCode = error.statusCode || 500;
  const statusMessage = error.statusMessage || "Server Error";
  const url = getRequestURL(event, { xForwardedHost: true, xForwardedProto: true });
  if (statusCode === 404) {
    const baseURL = "/";
    if (/^\/[^/]/.test(baseURL) && !url.pathname.startsWith(baseURL)) {
      const redirectTo = `${baseURL}${url.pathname.slice(1)}${url.search}`;
      return {
        status: 302,
        statusText: "Found",
        headers: { location: redirectTo },
        body: `Redirecting...`
      };
    }
  }
  if (isSensitive && !opts?.silent) {
    const tags = [error.unhandled && "[unhandled]", error.fatal && "[fatal]"].filter(Boolean).join(" ");
    console.error(`[request error] ${tags} [${event.method}] ${url}
`, error);
  }
  const headers = {
    "content-type": "application/json",
    // Prevent browser from guessing the MIME types of resources.
    "x-content-type-options": "nosniff",
    // Prevent error page from being embedded in an iframe
    "x-frame-options": "DENY",
    // Prevent browsers from sending the Referer header
    "referrer-policy": "no-referrer",
    // Disable the execution of any js
    "content-security-policy": "script-src 'none'; frame-ancestors 'none';"
  };
  setResponseStatus(event, statusCode, statusMessage);
  if (statusCode === 404 || !getResponseHeader(event, "cache-control")) {
    headers["cache-control"] = "no-cache";
  }
  const body = {
    error: true,
    url: url.href,
    statusCode,
    statusMessage,
    message: isSensitive ? "Server Error" : error.message,
    data: isSensitive ? void 0 : error.data
  };
  return {
    status: statusCode,
    statusText: statusMessage,
    headers,
    body
  };
}

const errorHandlers = [errorHandler$0, errorHandler$1];

async function errorHandler(error, event) {
  for (const handler of errorHandlers) {
    try {
      await handler(error, event, { defaultHandler });
      if (event.handled) {
        return; // Response handled
      }
    } catch(error) {
      // Handler itself thrown, log and continue
      console.error(error);
    }
  }
  // H3 will handle fallback
}

const plugins = [
  
];

const assets = {
  "/account.png": {
    "type": "image/png",
    "etag": "\"2a3-ztafiQrzVGWVtXeJXi1Az7Blsqc\"",
    "mtime": "2025-11-14T09:22:03.651Z",
    "size": 675,
    "path": "../public/account.png"
  },
  "/discord.svg": {
    "type": "image/svg+xml",
    "etag": "\"453-KGzy9TB+KHT45zEhjqboFQxH+m0\"",
    "mtime": "2025-11-14T09:22:03.650Z",
    "size": 1107,
    "path": "../public/discord.svg"
  },
  "/fallback-profile.webp": {
    "type": "image/webp",
    "etag": "\"46a8-mxkJNRY8adi0xmC70wDn4E3ZCWs\"",
    "mtime": "2025-11-14T09:22:03.653Z",
    "size": 18088,
    "path": "../public/fallback-profile.webp"
  },
  "/favicon.ico": {
    "type": "image/vnd.microsoft.icon",
    "etag": "\"877-Ves/YRtZhRrcklOt1gjDPGu9XYU\"",
    "mtime": "2025-11-14T09:22:03.653Z",
    "size": 2167,
    "path": "../public/favicon.ico"
  },
  "/gotify.png": {
    "type": "image/png",
    "etag": "\"c411-oahDMztCoPV4ojKsRAM3JgCD7iw\"",
    "mtime": "2025-11-14T09:22:03.653Z",
    "size": 50193,
    "path": "../public/gotify.png"
  },
  "/home-assistant.png": {
    "type": "image/png",
    "etag": "\"42fb-SozvL/xZqVCi9EEAwOng4ZZPRlw\"",
    "mtime": "2025-11-14T09:22:03.654Z",
    "size": 17147,
    "path": "../public/home-assistant.png"
  },
  "/icon.png": {
    "type": "image/png",
    "etag": "\"68d4-VMHWQqaE7VpUgtJaZE18n4XJJmE\"",
    "mtime": "2025-11-14T09:22:03.654Z",
    "size": 26836,
    "path": "../public/icon.png"
  },
  "/manifest.webmanifest": {
    "type": "application/manifest+json",
    "etag": "\"98e-kU1N+80i+w5EhmywhbU6V23e1fM\"",
    "mtime": "2025-11-14T09:22:03.238Z",
    "size": 2446,
    "path": "../public/manifest.webmanifest"
  },
  "/matrix.png": {
    "type": "image/png",
    "etag": "\"d86-EwE7XXB7cqgaKpRMcG2l+KKCAdM\"",
    "mtime": "2025-11-14T09:22:03.654Z",
    "size": 3462,
    "path": "../public/matrix.png"
  },
  "/mealie-email-banner.png": {
    "type": "image/png",
    "etag": "\"10413-i6sQAs5fuIiZOmXPmNYyMPTyoUM\"",
    "mtime": "2025-11-14T09:22:03.656Z",
    "size": 66579,
    "path": "../public/mealie-email-banner.png"
  },
  "/pushover.svg": {
    "type": "image/svg+xml",
    "etag": "\"d37-ppAmZcmGtEgPtgVSyGrkvDF4u1Y\"",
    "mtime": "2025-11-14T09:22:03.654Z",
    "size": 3383,
    "path": "../public/pushover.svg"
  },
  "/robots.txt": {
    "type": "text/plain; charset=utf-8",
    "etag": "\"18-xHzPGknCTMWEJDCqdccu9JEpJBI\"",
    "mtime": "2025-11-14T09:22:03.654Z",
    "size": 24,
    "path": "../public/robots.txt"
  },
  "/sw.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"52c2-LhdMoJQz+2p/o3JlC7uGN+M9cAE\"",
    "mtime": "2025-11-14T09:22:05.684Z",
    "size": 21186,
    "path": "../public/sw.js"
  },
  "/workbox-1e9cecc0.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3ab6-zXDlQkgrWEatYApiNPLMhnvXwT0\"",
    "mtime": "2025-11-14T09:22:05.685Z",
    "size": 15030,
    "path": "../public/workbox-1e9cecc0.js"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-4eGv4FsHdQO1qSioXxaUAVyyIMlPQLnNLNQbrzUmPMY.woff": {
    "type": "font/woff",
    "etag": "\"11fc0-O0pgror717QN7QxsJ1TyYrcXgIA\"",
    "mtime": "2025-11-14T09:22:03.247Z",
    "size": 73664,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-4eGv4FsHdQO1qSioXxaUAVyyIMlPQLnNLNQbrzUmPMY.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-4oe_Sj7BQtJqEEP8p8tlQHxZJJ52Po4KFX7_t9KAieA.woff": {
    "type": "font/woff",
    "etag": "\"10a14-fsh56JbjQTWLWhAxRjDG0IdQ4wc\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 68116,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-4oe_Sj7BQtJqEEP8p8tlQHxZJJ52Po4KFX7_t9KAieA.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-7qfpbeAG5o5p2sn_qCLMSWjA72jr0flw8iOpl6xVSDw.woff": {
    "type": "font/woff",
    "etag": "\"106d4-Z1YQ6cOTSCWxS8iz6VK+4RDnu4o\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 67284,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-7qfpbeAG5o5p2sn_qCLMSWjA72jr0flw8iOpl6xVSDw.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-Cemlm9u7NuW5vmOMpkRNyCwl83QLe9vkN8K3ySqlkwo.woff": {
    "type": "font/woff",
    "etag": "\"fe28-AYAAwOep0b151JzWVhzDegUZmKA\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 65064,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-Cemlm9u7NuW5vmOMpkRNyCwl83QLe9vkN8K3ySqlkwo.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-GOCgsFjKPub0CB03FfFbFLoTebLLrcgugxbMBJVfulU.woff": {
    "type": "font/woff",
    "etag": "\"11f68-Ex5c7xETKFnSVwSs7QGLMsiPmoc\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 73576,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-GOCgsFjKPub0CB03FfFbFLoTebLLrcgugxbMBJVfulU.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-MR_WnA2J1w-3hQJzXjEUxdRiVq92QSfLBsjEMAmyy3M.woff": {
    "type": "font/woff",
    "etag": "\"1187c-/pZ+y9IFCmJnQIbEUbO8Ksfw/9c\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 71804,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-MR_WnA2J1w-3hQJzXjEUxdRiVq92QSfLBsjEMAmyy3M.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-NCF3sA7nX2i_poQJYSNDMlGIs7D__lp17Ck7bDpcdjg.woff": {
    "type": "font/woff",
    "etag": "\"11d78-8dFs/tc14b5IggLKYmSZoKv+dBs\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 73080,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-NCF3sA7nX2i_poQJYSNDMlGIs7D__lp17Ck7bDpcdjg.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-One66783ILEh_aaSnr1U0QWydBY4f_J6iBxNDlPSbD8.woff": {
    "type": "font/woff",
    "etag": "\"10564-PmFynRN9DjSvIapdLirseQdqea4\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 66916,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-One66783ILEh_aaSnr1U0QWydBY4f_J6iBxNDlPSbD8.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-Op_oKG_MpuSr1oug4a1cj4apJtM-CaOA2L-Z3w4FmBw.woff": {
    "type": "font/woff",
    "etag": "\"10ff8-A4YegOKhyVOb+ZW5XiZJoYJmgO4\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 69624,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-Op_oKG_MpuSr1oug4a1cj4apJtM-CaOA2L-Z3w4FmBw.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-PqclKRI4jLCFS7vw4oHup1WImWAZMMcJrdaCk7bFQ40.woff": {
    "type": "font/woff",
    "etag": "\"11a00-HbSwESyPklBdbc8KKuv6MAdw3VU\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 72192,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-PqclKRI4jLCFS7vw4oHup1WImWAZMMcJrdaCk7bFQ40.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-boXQ6suSo9C2xrHQta8_S7b4q2rEp0cOsjZB2W-q7kA.woff": {
    "type": "font/woff",
    "etag": "\"11e78-P0G30cBpgq73TR2DXQAhSMB6CNg\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 73336,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-boXQ6suSo9C2xrHQta8_S7b4q2rEp0cOsjZB2W-q7kA.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-hAbi3X_1kTzKBNOSuNRV852FChFeGUm0aGzhVhV5L8A.woff": {
    "type": "font/woff",
    "etag": "\"11a0c-M+xKULmpuKNi9UuOqhebxbQ/jl4\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 72204,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-hAbi3X_1kTzKBNOSuNRV852FChFeGUm0aGzhVhV5L8A.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-pd_cycUs7fMxOGWSFwg9_CDHUt3_pcj0DEcGWA2POFg.woff": {
    "type": "font/woff",
    "etag": "\"10a08-+rlkJ/nQS9XfVP/FCFOpizk6fLY\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 68104,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-pd_cycUs7fMxOGWSFwg9_CDHUt3_pcj0DEcGWA2POFg.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-qFSHNKzDXJQ9RTFpl3_CVj7079_R_9gMPoZesmHuqw4.woff": {
    "type": "font/woff",
    "etag": "\"10950-Rw3TQpHuSZJwni53EOFGCzNrAjI\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 67920,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-qFSHNKzDXJQ9RTFpl3_CVj7079_R_9gMPoZesmHuqw4.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-rcFlADPPbCEQICFNwkRneodrif7gspVAntfmyPqxhYk.woff": {
    "type": "font/woff",
    "etag": "\"10414-P7zx7OWFGSVcTf2GkcvDJchaQ3I\"",
    "mtime": "2025-11-14T09:22:03.248Z",
    "size": 66580,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-rcFlADPPbCEQICFNwkRneodrif7gspVAntfmyPqxhYk.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-vTKRgjK_ncrz025TeurpgyWjYZx2t-UqvAu9Eoo2XMU.woff": {
    "type": "font/woff",
    "etag": "\"11fcc-f+acTNtxZhrOuZFxUL0+TI0zWjo\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 73676,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-vTKRgjK_ncrz025TeurpgyWjYZx2t-UqvAu9Eoo2XMU.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-vhiRB78GS3OtXU2XVKuaczmW55Ttgi_IRu8dTPW9yls.woff": {
    "type": "font/woff",
    "etag": "\"10a24-k5Yc/vUhGI8vCVY35P3tRV0jHbQ\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 68132,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-vhiRB78GS3OtXU2XVKuaczmW55Ttgi_IRu8dTPW9yls.woff"
  },
  "/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-xWbXGi4xNs9mg4OxQlfYOigm3pJCVnTT8GM5yb6zovk.woff": {
    "type": "font/woff",
    "etag": "\"10558-3aPvbcrFT8Ud/lPPnX6qWU5ZTeU\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 66904,
    "path": "../public/_fonts/1ZTlEDqU4DtwDJiND8f6qaugUpa0RIDvQl-v7iM6l54-xWbXGi4xNs9mg4OxQlfYOigm3pJCVnTT8GM5yb6zovk.woff"
  },
  "/_fonts/6gxaoD7DQeGZTK54nUXSkdRWC0c-wCuX7MyFieq-1K8-Oq_mSHEboaD9Dg7CDn9BrkGVJk_UOJhKReOqHILcKPQ.woff2": {
    "type": "font/woff2",
    "etag": "\"3b68-35T0F1vXJH6ason5/XHCT8x+yy0\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 15208,
    "path": "../public/_fonts/6gxaoD7DQeGZTK54nUXSkdRWC0c-wCuX7MyFieq-1K8-Oq_mSHEboaD9Dg7CDn9BrkGVJk_UOJhKReOqHILcKPQ.woff2"
  },
  "/_fonts/BytOw1WpauQKDI26Z7Zi_jjmRfrbDnjpWxdiylsqHmY-NVE3r0DxQZ4G7vbNS2tAhmbM6o2QgcyRSuW3LwEM1jc.woff2": {
    "type": "font/woff2",
    "etag": "\"5088-1rSKdNgggB51UQ66lqbmGiOwGMY\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 20616,
    "path": "../public/_fonts/BytOw1WpauQKDI26Z7Zi_jjmRfrbDnjpWxdiylsqHmY-NVE3r0DxQZ4G7vbNS2tAhmbM6o2QgcyRSuW3LwEM1jc.woff2"
  },
  "/_fonts/DjqLtQmWy3Sy26TlSZoazWKlNJfaXSyR1J7pZxNm01w-_P6Bw1Mj9huIZUf8qHk0dhKzXZouYFsfd6DChSFpKqQ.woff2": {
    "type": "font/woff2",
    "etag": "\"86bc-61EQ3vf/3ah3IuofI/yM+DCkkhs\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 34492,
    "path": "../public/_fonts/DjqLtQmWy3Sy26TlSZoazWKlNJfaXSyR1J7pZxNm01w-_P6Bw1Mj9huIZUf8qHk0dhKzXZouYFsfd6DChSFpKqQ.woff2"
  },
  "/_fonts/EMrLSPWTh0rHKutQg0CRbT-6CC-7ZCUXI8mUB5xsUzA-ewwiX1GJMsXOIlA9Lnd5BdxQq83r73NSgDgyLq9wmOk.woff2": {
    "type": "font/woff2",
    "etag": "\"40a4-UYTSFaKpCIclshy4vkHhTyb5lKI\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 16548,
    "path": "../public/_fonts/EMrLSPWTh0rHKutQg0CRbT-6CC-7ZCUXI8mUB5xsUzA-ewwiX1GJMsXOIlA9Lnd5BdxQq83r73NSgDgyLq9wmOk.woff2"
  },
  "/_fonts/H2FXkDRX4aGYE7pLEuvYkNHQSqxd4MIt2393pduYjiU-K_3LJwzu8AZDDGqiyuZAgYoidLGyB5tww9gLpZHA1P4.woff2": {
    "type": "font/woff2",
    "etag": "\"876c-MAo1ERAKLqH79DvzKYVeF9ofRTI\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 34668,
    "path": "../public/_fonts/H2FXkDRX4aGYE7pLEuvYkNHQSqxd4MIt2393pduYjiU-K_3LJwzu8AZDDGqiyuZAgYoidLGyB5tww9gLpZHA1P4.woff2"
  },
  "/_fonts/JGpV_UcLP8V5a1WH2PeMgam0F8KzAc-NHgo22tNt244-e_afzLbI2kgnBTFeFJBgGMmGOadlNO3Igp_DMlVc18Q.woff2": {
    "type": "font/woff2",
    "etag": "\"27ac-wcm6utp61ntN4eBHS7XeOOHl1ug\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 10156,
    "path": "../public/_fonts/JGpV_UcLP8V5a1WH2PeMgam0F8KzAc-NHgo22tNt244-e_afzLbI2kgnBTFeFJBgGMmGOadlNO3Igp_DMlVc18Q.woff2"
  },
  "/_fonts/QdUA0WfUO-WPJcIRrsY44o3ueRi_9-EsQTU36CIkDoc-BS4tplKtsw64JXEAvesbVatWNQoour_XgJdbbKJiFLA.woff2": {
    "type": "font/woff2",
    "etag": "\"243c-Y8oS9jweBp8VwX+i7AzkBI3IfF4\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 9276,
    "path": "../public/_fonts/QdUA0WfUO-WPJcIRrsY44o3ueRi_9-EsQTU36CIkDoc-BS4tplKtsw64JXEAvesbVatWNQoour_XgJdbbKJiFLA.woff2"
  },
  "/_fonts/WFnd9i24bHwwi9nCxDYKKobwMl6TIN-k117y2K8oGC4-EGkG2XoDEDhEIXoK_AmRJntlqK4NgsJDGkm_z3PlAtQ.woff2": {
    "type": "font/woff2",
    "etag": "\"53c0-6KG3LRu2CUk2j5jO/nHGr2th2PY\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 21440,
    "path": "../public/_fonts/WFnd9i24bHwwi9nCxDYKKobwMl6TIN-k117y2K8oGC4-EGkG2XoDEDhEIXoK_AmRJntlqK4NgsJDGkm_z3PlAtQ.woff2"
  },
  "/_fonts/XDL4h8cIroh1AI30355-6EdXC4VLRTJDQEFnBxyrruE-_1j_5J1TCJ8T0YtJrHyz-dLABPp9bPOle-VnPdz1y6s.woff2": {
    "type": "font/woff2",
    "etag": "\"76d8-YM0HYw0XPifDMffapHxKUHMtxDk\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 30424,
    "path": "../public/_fonts/XDL4h8cIroh1AI30355-6EdXC4VLRTJDQEFnBxyrruE-_1j_5J1TCJ8T0YtJrHyz-dLABPp9bPOle-VnPdz1y6s.woff2"
  },
  "/_fonts/Yr7HGIjsxw1ejDRZ1fDEK_uI9N9oVX--72BOJvhGns0-C9X9ewDmcT4HrCq1rIM7rQhnYYvDuzg_qMi1KGPN9pQ.woff2": {
    "type": "font/woff2",
    "etag": "\"96a0-iYN76OdqhUh0NGjcFt0HMBB+CuU\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 38560,
    "path": "../public/_fonts/Yr7HGIjsxw1ejDRZ1fDEK_uI9N9oVX--72BOJvhGns0-C9X9ewDmcT4HrCq1rIM7rQhnYYvDuzg_qMi1KGPN9pQ.woff2"
  },
  "/_fonts/auXPe3ZKiUcEpUCV6WUns9YnBBbTsWuKwtesi_8WLJQ-SM1Db39G4j_TENhpci6yMzXOiyLVqlS0OKlllGY8mqg.woff2": {
    "type": "font/woff2",
    "etag": "\"49a4-bGpYPUYaSBV1EtWFvW8MK+Wuamg\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 18852,
    "path": "../public/_fonts/auXPe3ZKiUcEpUCV6WUns9YnBBbTsWuKwtesi_8WLJQ-SM1Db39G4j_TENhpci6yMzXOiyLVqlS0OKlllGY8mqg.woff2"
  },
  "/_fonts/gAUuOnKdT3UqEgWcFzAGXVXhLJCLnuRcUz1vhLLJsGw-tSI9aXvrBp5uJ1W2zi8aV56Ha40g6JGO5vW0oAmNGmk.woff2": {
    "type": "font/woff2",
    "etag": "\"4810-ijS4iuzJ6G2GKj4fzOtQtQVRHS0\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 18448,
    "path": "../public/_fonts/gAUuOnKdT3UqEgWcFzAGXVXhLJCLnuRcUz1vhLLJsGw-tSI9aXvrBp5uJ1W2zi8aV56Ha40g6JGO5vW0oAmNGmk.woff2"
  },
  "/_fonts/hwdBUbneWNnoMlJaBBo8lCMnw9j_Ex7FrYBFoMmAb6Q-qpOLWPz5Pr_P3S1F64TTQKR8YDChUi4xIstAY6dhOf4.woff2": {
    "type": "font/woff2",
    "etag": "\"62c-RLJ6+64IjSatpILYDW5Sr9upNNg\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 1580,
    "path": "../public/_fonts/hwdBUbneWNnoMlJaBBo8lCMnw9j_Ex7FrYBFoMmAb6Q-qpOLWPz5Pr_P3S1F64TTQKR8YDChUi4xIstAY6dhOf4.woff2"
  },
  "/_fonts/jnTaqgqIXQJvRvZjoADo4u9rPrHhIg9x0Pkby2MksBA-WKm_ey2ddERYy8I00wBF9qpzH0dYfkcdkAsXurxwO_8.woff2": {
    "type": "font/woff2",
    "etag": "\"5c80-qsPzZNTm8SM9w6kdIpIwysBtQW4\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 23680,
    "path": "../public/_fonts/jnTaqgqIXQJvRvZjoADo4u9rPrHhIg9x0Pkby2MksBA-WKm_ey2ddERYy8I00wBF9qpzH0dYfkcdkAsXurxwO_8.woff2"
  },
  "/_fonts/n872X1k0xVGHVuWVumTB90UU935PLWlUb-QbVkg5nVo-1ghf6tPF_WrZUIM_KGqh510Vm3G3X8OpJ5UjwWm4oYA.woff2": {
    "type": "font/woff2",
    "etag": "\"9970-aieRHKILTCha1yNIUW/VTk/lniI\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 39280,
    "path": "../public/_fonts/n872X1k0xVGHVuWVumTB90UU935PLWlUb-QbVkg5nVo-1ghf6tPF_WrZUIM_KGqh510Vm3G3X8OpJ5UjwWm4oYA.woff2"
  },
  "/_fonts/pFVHc1vdPmKUOVbC-oPNlu579jq898KZ6kByQAibRcM-MtEpPmPa_NQa2JQYaAFAToMhplqMnfsGAvkwVj3pOrk.woff2": {
    "type": "font/woff2",
    "etag": "\"3680-N7Twzs5S0UnVdnBWyWQHjZdIWVI\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 13952,
    "path": "../public/_fonts/pFVHc1vdPmKUOVbC-oPNlu579jq898KZ6kByQAibRcM-MtEpPmPa_NQa2JQYaAFAToMhplqMnfsGAvkwVj3pOrk.woff2"
  },
  "/_fonts/qFfsvWamVvQ82W1UHje2avdvsmuGh4qR7PWBbcMLc8s-9XW0QeVhDgnpYOkCqcuaK5iELM8xqN8d3UWZ8ikOvS4.woff2": {
    "type": "font/woff2",
    "etag": "\"8ac8-dONRo94Th/jYzt3L9N9tfEBknZc\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 35528,
    "path": "../public/_fonts/qFfsvWamVvQ82W1UHje2avdvsmuGh4qR7PWBbcMLc8s-9XW0QeVhDgnpYOkCqcuaK5iELM8xqN8d3UWZ8ikOvS4.woff2"
  },
  "/_fonts/yh0ak2-oYBSnZxDNj3bqXlr-CViKiu-xNROahZJAseA-NLz6nXggOOZ114SAmE7BiDe_6Kby_wPe-1qqYNvzDQc.woff2": {
    "type": "font/woff2",
    "etag": "\"6c4-M3J9p0Aflvojrt0mu0XIFuo9PsA\"",
    "mtime": "2025-11-14T09:22:03.249Z",
    "size": 1732,
    "path": "../public/_fonts/yh0ak2-oYBSnZxDNj3bqXlr-CViKiu-xNROahZJAseA-NLz6nXggOOZ114SAmE7BiDe_6Kby_wPe-1qqYNvzDQc.woff2"
  },
  "/icons/android-chrome-192x192.png": {
    "type": "image/png",
    "etag": "\"14d5-t9iGKh0I1QUmtMFqqkLG/eHLyRs\"",
    "mtime": "2025-11-14T09:22:03.392Z",
    "size": 5333,
    "path": "../public/icons/android-chrome-192x192.png"
  },
  "/icons/android-chrome-512x512.png": {
    "type": "image/png",
    "etag": "\"39b4-zLinsTusDhi32csuB4ViP2pvoEw\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 14772,
    "path": "../public/icons/android-chrome-512x512.png"
  },
  "/icons/android-chrome-maskable-192x192.png": {
    "type": "image/png",
    "etag": "\"db3-xi4MfQi0KAj8n9XVa3NOWoVOMOU\"",
    "mtime": "2025-11-14T09:22:03.542Z",
    "size": 3507,
    "path": "../public/icons/android-chrome-maskable-192x192.png"
  },
  "/icons/android-chrome-maskable-512x512.png": {
    "type": "image/png",
    "etag": "\"258f-ByEFd+9RZrjH5I8i2sP3d2rM2Jg\"",
    "mtime": "2025-11-14T09:22:03.640Z",
    "size": 9615,
    "path": "../public/icons/android-chrome-maskable-512x512.png"
  },
  "/icons/apple-touch-icon.png": {
    "type": "image/png",
    "etag": "\"a52-2OBfpaTnwcDWOdh0vhBzZuGPt1k\"",
    "mtime": "2025-11-14T09:22:03.429Z",
    "size": 2642,
    "path": "../public/icons/apple-touch-icon.png"
  },
  "/icons/favicon-16x16.png": {
    "type": "image/png",
    "etag": "\"373-hdNeN8If3YgKHK/+4x0qJ5Nbko4\"",
    "mtime": "2025-11-14T09:22:03.429Z",
    "size": 883,
    "path": "../public/icons/favicon-16x16.png"
  },
  "/icons/favicon-32x32.png": {
    "type": "image/png",
    "etag": "\"469-9FE3DdZNxOYdVBqi8DbuzNM9xnI\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 1129,
    "path": "../public/icons/favicon-32x32.png"
  },
  "/icons/icon-x64.png": {
    "type": "image/png",
    "etag": "\"2a51-yu6p0XcoYpnZ+XI27Jzz1ybzBlE\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 10833,
    "path": "../public/icons/icon-x64.png"
  },
  "/icons/mdiCalendarMultiselect-192x192.png": {
    "type": "image/png",
    "etag": "\"5d7-leiC+h+GRLENIq3SrxWomZap/pU\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 1495,
    "path": "../public/icons/mdiCalendarMultiselect-192x192.png"
  },
  "/icons/mdiCalendarMultiselect-96x96.png": {
    "type": "image/png",
    "etag": "\"303-Tx5Y2w24VhJACDBhjN5hhF2pbNY\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 771,
    "path": "../public/icons/mdiCalendarMultiselect-96x96.png"
  },
  "/icons/mdiFormatListChecks-192x192.png": {
    "type": "image/png",
    "etag": "\"532-c8CjAhBHCA7ygjA5NStLzcCiM/o\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 1330,
    "path": "../public/icons/mdiFormatListChecks-192x192.png"
  },
  "/icons/mdiFormatListChecks-96x96.png": {
    "type": "image/png",
    "etag": "\"2f8-S+AK0KoqZWjkuli5H5bRy/SkBe8\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 760,
    "path": "../public/icons/mdiFormatListChecks-96x96.png"
  },
  "/icons/mstile-150x150.png": {
    "type": "image/png",
    "etag": "\"9e2-ap7mku3xtkY24xfhXS0wbcej2UI\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 2530,
    "path": "../public/icons/mstile-150x150.png"
  },
  "/icons/safari-pinned-tab.svg": {
    "type": "image/svg+xml",
    "etag": "\"629-98b2NJUT+31agEsu+7iLYCgTi+0\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 1577,
    "path": "../public/icons/safari-pinned-tab.svg"
  },
  "/screenshots/editor-narrow.png": {
    "type": "image/png",
    "etag": "\"35c91-iAu399/Gk5RHjJZJT0C7T0NF5s4\"",
    "mtime": "2025-11-14T09:22:03.430Z",
    "size": 220305,
    "path": "../public/screenshots/editor-narrow.png"
  },
  "/screenshots/editor-wide.png": {
    "type": "image/png",
    "etag": "\"20842-k+5fw1ergy5mkCGL0GtTYxdN2BU\"",
    "mtime": "2025-11-14T09:22:03.498Z",
    "size": 133186,
    "path": "../public/screenshots/editor-wide.png"
  },
  "/screenshots/home-narrow.png": {
    "type": "image/png",
    "etag": "\"11f25c-eNxHhk49LYpC7BDYXzioTyuiPb4\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 1176156,
    "path": "../public/screenshots/home-narrow.png"
  },
  "/screenshots/home-wide.png": {
    "type": "image/png",
    "etag": "\"1dafb7-IVgHLOejvQ5gX4QlAASid7pAtlg\"",
    "mtime": "2025-11-14T09:22:03.654Z",
    "size": 1945527,
    "path": "../public/screenshots/home-wide.png"
  },
  "/screenshots/parser-narrow.png": {
    "type": "image/png",
    "etag": "\"2347e-NIFhuXzRP00fofBcojFFEbgcuv0\"",
    "mtime": "2025-11-14T09:22:03.498Z",
    "size": 144510,
    "path": "../public/screenshots/parser-narrow.png"
  },
  "/screenshots/parser-wide.png": {
    "type": "image/png",
    "etag": "\"2c27b-oPrc03dDbzCLWP0cdsyo1B9dIGs\"",
    "mtime": "2025-11-14T09:22:03.498Z",
    "size": 180859,
    "path": "../public/screenshots/parser-wide.png"
  },
  "/screenshots/recipe-narrow.png": {
    "type": "image/png",
    "etag": "\"c080d-jWJ3zgXAYo/it9FC2tbNmONgTqs\"",
    "mtime": "2025-11-14T09:22:03.650Z",
    "size": 788493,
    "path": "../public/screenshots/recipe-narrow.png"
  },
  "/screenshots/recipe-wide.png": {
    "type": "image/png",
    "etag": "\"ebb60-dO5nw8nWb9NkXixy9cygl5VVDt4\"",
    "mtime": "2025-11-14T09:22:03.650Z",
    "size": 965472,
    "path": "../public/screenshots/recipe-wide.png"
  },
  "/svgs/admin-site-settings.svg": {
    "type": "image/svg+xml",
    "etag": "\"5473-6SpycM1L9XzUeVq5yzjyTdXzDzQ\"",
    "mtime": "2025-11-14T09:22:03.391Z",
    "size": 21619,
    "path": "../public/svgs/admin-site-settings.svg"
  },
  "/svgs/data-reports.svg": {
    "type": "image/svg+xml",
    "etag": "\"1ede-5jHjutmqnA3WHiNlR/grOzBySvw\"",
    "mtime": "2025-11-14T09:22:03.542Z",
    "size": 7902,
    "path": "../public/svgs/data-reports.svg"
  },
  "/svgs/manage-api-tokens.svg": {
    "type": "image/svg+xml",
    "etag": "\"56d4-uM0yZU77joLftBWH5G47xl2qwQc\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 22228,
    "path": "../public/svgs/manage-api-tokens.svg"
  },
  "/svgs/manage-cookbooks.svg": {
    "type": "image/svg+xml",
    "etag": "\"4158-IktiK7h9P0aHo9TsO42jm1dSYC4\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 16728,
    "path": "../public/svgs/manage-cookbooks.svg"
  },
  "/svgs/manage-data-migrations.svg": {
    "type": "image/svg+xml",
    "etag": "\"4014-jgr6dnwXKnZvk5mmZNrnvwZDeng\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 16404,
    "path": "../public/svgs/manage-data-migrations.svg"
  },
  "/svgs/manage-group-settings.svg": {
    "type": "image/svg+xml",
    "etag": "\"2b14-GpuZBbxMuqCNpBHnZZ7c4YGFHS0\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 11028,
    "path": "../public/svgs/manage-group-settings.svg"
  },
  "/svgs/manage-members.svg": {
    "type": "image/svg+xml",
    "etag": "\"909b-a5o8bVKCn/CSS2O0gCgqLsY9PF0\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 37019,
    "path": "../public/svgs/manage-members.svg"
  },
  "/svgs/manage-notifiers.svg": {
    "type": "image/svg+xml",
    "etag": "\"24bf-fLe+w5xHiC9NZnYWtD2jKoxJ/NE\"",
    "mtime": "2025-11-14T09:22:03.628Z",
    "size": 9407,
    "path": "../public/svgs/manage-notifiers.svg"
  },
  "/svgs/manage-profile.svg": {
    "type": "image/svg+xml",
    "etag": "\"3411-dHGCl1/FUxuiNHlouX8tUwAwi78\"",
    "mtime": "2025-11-14T09:22:03.629Z",
    "size": 13329,
    "path": "../public/svgs/manage-profile.svg"
  },
  "/svgs/manage-recipes.svg": {
    "type": "image/svg+xml",
    "etag": "\"2541-UQd+h20w8vT29NrNtPC82CWAnuQ\"",
    "mtime": "2025-11-14T09:22:03.640Z",
    "size": 9537,
    "path": "../public/svgs/manage-recipes.svg"
  },
  "/svgs/manage-tasks.svg": {
    "type": "image/svg+xml",
    "etag": "\"269f-vFyDh33fMskSoHgdMaU16TKTxHQ\"",
    "mtime": "2025-11-14T09:22:03.640Z",
    "size": 9887,
    "path": "../public/svgs/manage-tasks.svg"
  },
  "/svgs/manage-webhooks.svg": {
    "type": "image/svg+xml",
    "etag": "\"1007-HMa7LpPH62fD7UoIIgjMqcvK8LQ\"",
    "mtime": "2025-11-14T09:22:03.640Z",
    "size": 4103,
    "path": "../public/svgs/manage-webhooks.svg"
  },
  "/svgs/recipes-create.svg": {
    "type": "image/svg+xml",
    "etag": "\"210c-Rn5w3c9SUPrWuBtvzH1Lzxo0unk\"",
    "mtime": "2025-11-14T09:22:03.640Z",
    "size": 8460,
    "path": "../public/svgs/recipes-create.svg"
  },
  "/svgs/shopping-cart.svg": {
    "type": "image/svg+xml",
    "etag": "\"23ba-YBk+CNxcqxWkVncbuCT0ISpXZTU\"",
    "mtime": "2025-11-14T09:22:03.640Z",
    "size": 9146,
    "path": "../public/svgs/shopping-cart.svg"
  },
  "/_nuxt/-WV2njIR.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"15d8-zZ+pZhV1DY3+UkHYTC0MrEWb45w\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 5592,
    "path": "../public/_nuxt/-WV2njIR.js"
  },
  "/_nuxt/-Zgi00g_.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4323-LXcXL/Fn7eFU6O0cNnxUjAhdHko\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 17187,
    "path": "../public/_nuxt/-Zgi00g_.js"
  },
  "/_nuxt/0-8fZDLc.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-9qyggne2X8MeElVS7bpMM/rDDbw\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 477,
    "path": "../public/_nuxt/0-8fZDLc.js"
  },
  "/_nuxt/0JpLA9kZ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-PMRq2T4wgeIIBjefX/NUObz4GXs\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 477,
    "path": "../public/_nuxt/0JpLA9kZ.js"
  },
  "/_nuxt/1ZadaH8c.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"99b-YyLbK4CLtAyfsb+ZG1ra2vgaLYE\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 2459,
    "path": "../public/_nuxt/1ZadaH8c.js"
  },
  "/_nuxt/25sUHL9t.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"427-yICjFwJCCOoI/BmZlKr3gMO5mg4\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 1063,
    "path": "../public/_nuxt/25sUHL9t.js"
  },
  "/_nuxt/5PE8rzvJ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1288-gnJbmEs9zYrWlZAC2K3ho8oodHI\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 4744,
    "path": "../public/_nuxt/5PE8rzvJ.js"
  },
  "/_nuxt/6--iqVZy.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"67-QKYf6rBv97Z1FMhcdwQxQm1zUkg\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 103,
    "path": "../public/_nuxt/6--iqVZy.js"
  },
  "/_nuxt/61n8pI5Z.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"33f-3RooAjbwXiJue6MLkJIOuFUaMfs\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 831,
    "path": "../public/_nuxt/61n8pI5Z.js"
  },
  "/_nuxt/64LGVOuc.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4cf-WfuU4RSWD3NW8oAqgjBHsFaAKKw\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 1231,
    "path": "../public/_nuxt/64LGVOuc.js"
  },
  "/_nuxt/6p1Qu8T5.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"173-h1wpxbHxUd0QIXclSCkC9Ltua3M\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 371,
    "path": "../public/_nuxt/6p1Qu8T5.js"
  },
  "/_nuxt/8279AkRy.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"297a-hmQvxpKm1QqkBlinHLQDqFDzM8k\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 10618,
    "path": "../public/_nuxt/8279AkRy.js"
  },
  "/_nuxt/8f9Pbnz8.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-xaDFFMfclqJQEI06TIAxpB2s9VM\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 477,
    "path": "../public/_nuxt/8f9Pbnz8.js"
  },
  "/_nuxt/9QQk8D7F.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"560-n+09NL+pXLbRrk14gqi9YSNqXlo\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 1376,
    "path": "../public/_nuxt/9QQk8D7F.js"
  },
  "/_nuxt/9soh8dYU.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1234d-R/pEzZC7LRGWVrKxvG8NE3raq3g\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 74573,
    "path": "../public/_nuxt/9soh8dYU.js"
  },
  "/_nuxt/A7h89_1a.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-7fxNknDIU22FEtv4iTA0BD3Faac\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 477,
    "path": "../public/_nuxt/A7h89_1a.js"
  },
  "/_nuxt/ASFe71zB.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"b5a-IdYuMH8SsG6ATRRDOVYIntO6Y+k\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 2906,
    "path": "../public/_nuxt/ASFe71zB.js"
  },
  "/_nuxt/AcIOyaSj.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13083-tXtYHNl8K0PNBW0kH7KNmIk8X1k\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 77955,
    "path": "../public/_nuxt/AcIOyaSj.js"
  },
  "/_nuxt/AppHeader.DqSqaKQo.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"4c-Po9XbxMee/67JsnPa4kD0Gsb2EE\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 76,
    "path": "../public/_nuxt/AppHeader.DqSqaKQo.css"
  },
  "/_nuxt/AppLogo.EwDlndIc.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"117-5DU6AaQKjr4wsyHhdTKoG38zPCU\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 279,
    "path": "../public/_nuxt/AppLogo.EwDlndIc.css"
  },
  "/_nuxt/AppSidebar.fzNSX130.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"953-T8edQZgJdrCmHHEFV+XH1YfP9oc\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 2387,
    "path": "../public/_nuxt/AppSidebar.fzNSX130.css"
  },
  "/_nuxt/B0cqqxPl.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11fcb-PRKJcWeOuuhZ2Ahv5xyiFBOJzpI\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 73675,
    "path": "../public/_nuxt/B0cqqxPl.js"
  },
  "/_nuxt/B0hyceY3.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"406-ReujZflUk5np4aps8cpeV4HmPtE\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 1030,
    "path": "../public/_nuxt/B0hyceY3.js"
  },
  "/_nuxt/B1P6H5Bk.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"f7-YCB2WuRzU4iHKA3G/Ddi07FSNKI\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 247,
    "path": "../public/_nuxt/B1P6H5Bk.js"
  },
  "/_nuxt/B30FjQBc.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9cd-/UiCL17Zfr4NlvGi17VxNEHMi/0\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 2509,
    "path": "../public/_nuxt/B30FjQBc.js"
  },
  "/_nuxt/B3DrhHGV.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-7Q0ELPVoE0OYwuTIssSKV73oc48\"",
    "mtime": "2025-11-14T09:22:03.364Z",
    "size": 477,
    "path": "../public/_nuxt/B3DrhHGV.js"
  },
  "/_nuxt/B3LgXoKV.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"48a3-2H7u8mE4375xxbjU2HojfVSR61s\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 18595,
    "path": "../public/_nuxt/B3LgXoKV.js"
  },
  "/_nuxt/B41xnvqz.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"774-JRvneRsKLaHIWz05a6hYef5URxs\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1908,
    "path": "../public/_nuxt/B41xnvqz.js"
  },
  "/_nuxt/B5nOiJkU.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"ee8-i/bbUYeoNCha9/45Eg99tOMVjjA\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 3816,
    "path": "../public/_nuxt/B5nOiJkU.js"
  },
  "/_nuxt/B66Xma2s.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"124a-KFZVJZmV5l6DMiUbWZiLWPdbV4s\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 4682,
    "path": "../public/_nuxt/B66Xma2s.js"
  },
  "/_nuxt/B7aulykK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"6b70-Lge33cah/TVVmeNlaX/2QoRjwxk\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 27504,
    "path": "../public/_nuxt/B7aulykK.js"
  },
  "/_nuxt/B7jl-kVx.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"aa0-fMRxNQ+CluOtnQlE63nlLKdb8J8\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 2720,
    "path": "../public/_nuxt/B7jl-kVx.js"
  },
  "/_nuxt/B8Bozi2G.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"495-ozhNP0K2zypBXbUTLf587itpYZA\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1173,
    "path": "../public/_nuxt/B8Bozi2G.js"
  },
  "/_nuxt/BAF5Up4h.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"161e-zcM52BIIs6lKX/knSh4foWezSG4\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 5662,
    "path": "../public/_nuxt/BAF5Up4h.js"
  },
  "/_nuxt/BBqk0Sce.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3e54-RcqMlN+fGwm3XqjgY1PymgmOV14\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 15956,
    "path": "../public/_nuxt/BBqk0Sce.js"
  },
  "/_nuxt/BCst9DHX.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5f-T7wY1FM4GBHqH67k5yuQlBYo0ns\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 95,
    "path": "../public/_nuxt/BCst9DHX.js"
  },
  "/_nuxt/BD5x-Klm.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2fb-HbzhvxcWUlipQJk3gxqEim4d1o0\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 763,
    "path": "../public/_nuxt/BD5x-Klm.js"
  },
  "/_nuxt/BFSXoCTX.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"7a1-HGcsD3iMK+yYkFq/HFGzkohWptY\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1953,
    "path": "../public/_nuxt/BFSXoCTX.js"
  },
  "/_nuxt/BFUcKmee.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-TINumlj/Rq5TBCgnM9vglR/kM+8\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 477,
    "path": "../public/_nuxt/BFUcKmee.js"
  },
  "/_nuxt/BFyg-RCw.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"f80-c0/sG9brVpfhyv6sHfruV8C3DxM\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 3968,
    "path": "../public/_nuxt/BFyg-RCw.js"
  },
  "/_nuxt/BG7KPWkA.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5ae-oFDSpBBU5MVmbrYKIZb79qMACCI\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1454,
    "path": "../public/_nuxt/BG7KPWkA.js"
  },
  "/_nuxt/BHRwmCuG.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"123b0-f9D0UQJLl77zNmKyKFnoBRE4xig\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 74672,
    "path": "../public/_nuxt/BHRwmCuG.js"
  },
  "/_nuxt/BIOzsZIs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"b6f-+SuQVCp8r8fimFrS+Sg9jeRCCyg\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 2927,
    "path": "../public/_nuxt/BIOzsZIs.js"
  },
  "/_nuxt/BIy6ZRku.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-L2k/X3nLjeJhn28s/+ID6KNmFBs\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 477,
    "path": "../public/_nuxt/BIy6ZRku.js"
  },
  "/_nuxt/BJD0DYNW.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1196ba-bbicqA5JSeclnXmI5T503MaAOAY\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 1152698,
    "path": "../public/_nuxt/BJD0DYNW.js"
  },
  "/_nuxt/BJR0ny-J.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-LHDRwdZU995GbLBEuUPistXjZq4\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 477,
    "path": "../public/_nuxt/BJR0ny-J.js"
  },
  "/_nuxt/BK_qGue2.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"144bc-V1ieqOP0VudfbRaHFg0naq2E2Aw\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 83132,
    "path": "../public/_nuxt/BK_qGue2.js"
  },
  "/_nuxt/BLi4IIk3.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"414-2qD786Pgso5vwhkJ70SzqJJhxn4\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1044,
    "path": "../public/_nuxt/BLi4IIk3.js"
  },
  "/_nuxt/BLuTasLz.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"99-AzINTEkldGyWPKfAKfSiOVKr67o\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 153,
    "path": "../public/_nuxt/BLuTasLz.js"
  },
  "/_nuxt/BO2q3KCQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"65d-fFmH5sWu8SCfl+ffILenNgBwr/M\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1629,
    "path": "../public/_nuxt/BO2q3KCQ.js"
  },
  "/_nuxt/BSBm8mzt.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"7b0-5BG2WSZL8hSrEHM01QiqFF4iycQ\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1968,
    "path": "../public/_nuxt/BSBm8mzt.js"
  },
  "/_nuxt/BSNtjwdl.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"17c5-rM+lofAvuANPwcU/lsFxcXXNH6A\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 6085,
    "path": "../public/_nuxt/BSNtjwdl.js"
  },
  "/_nuxt/BTHUibnE.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2396-jnqrvOlH4eQ3UNvAkObDcZqhtqs\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 9110,
    "path": "../public/_nuxt/BTHUibnE.js"
  },
  "/_nuxt/BU5n-m2V.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"91a-Ktvo9QwX/f1TlXkaW5ccktozw0g\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 2330,
    "path": "../public/_nuxt/BU5n-m2V.js"
  },
  "/_nuxt/BU77RRT5.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"72c-IW4ugR5INMaEUyFRys5kwC5CFiE\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 1836,
    "path": "../public/_nuxt/BU77RRT5.js"
  },
  "/_nuxt/BVRUsyWl.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"315-kOCGnAq2agL87oMJ25IwEnHgaS8\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 789,
    "path": "../public/_nuxt/BVRUsyWl.js"
  },
  "/_nuxt/BVhWUuIB.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"399-4mtNPB2yeOQjPWm5KEbDXKmqjfI\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 921,
    "path": "../public/_nuxt/BVhWUuIB.js"
  },
  "/_nuxt/BW3tTUjO.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"58-AYFZb6bhpa4incy5zRyLX7R/ooA\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 88,
    "path": "../public/_nuxt/BW3tTUjO.js"
  },
  "/_nuxt/BWdoiWQ_.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"80b-p8qkTcDrq00wsYz0TVPsx19rRMQ\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 2059,
    "path": "../public/_nuxt/BWdoiWQ_.js"
  },
  "/_nuxt/BYRe52N2.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c5c-epw6XlFTscVWvnK9XvMm1BTch98\"",
    "mtime": "2025-11-14T09:22:03.365Z",
    "size": 3164,
    "path": "../public/_nuxt/BYRe52N2.js"
  },
  "/_nuxt/B_AHKV-3.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"8b9-R5GLYagt98O0Qn2HqowIgBIetfU\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 2233,
    "path": "../public/_nuxt/B_AHKV-3.js"
  },
  "/_nuxt/B_Xo5VNZ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13fc-Y696OjpHJRj75QnVKY4fio+bxFA\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 5116,
    "path": "../public/_nuxt/B_Xo5VNZ.js"
  },
  "/_nuxt/Ba4GrxJ3.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1e5-IPDqxQRVL/sIsWOcuWHFCrei3Q8\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 485,
    "path": "../public/_nuxt/Ba4GrxJ3.js"
  },
  "/_nuxt/Ba8M5IUy.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-9IBrmCAH/QSBApphftHhu/cZRTU\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 477,
    "path": "../public/_nuxt/Ba8M5IUy.js"
  },
  "/_nuxt/BaseButtonGroup.D-0vg8zC.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"65-IN2r/XvkJIEQ5JtBC4BG/jh0Qy8\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 101,
    "path": "../public/_nuxt/BaseButtonGroup.D-0vg8zC.css"
  },
  "/_nuxt/BaseDialog.CAWfojTc.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"22-4rISm1HWEwhfKT6iArv/r0ZaCmQ\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 34,
    "path": "../public/_nuxt/BaseDialog.CAWfojTc.css"
  },
  "/_nuxt/BasePageTitle.AiN4IQ0i.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"59-AK8IFiteubp/qkVGKTpEa/kgG+s\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 89,
    "path": "../public/_nuxt/BasePageTitle.AiN4IQ0i.css"
  },
  "/_nuxt/BbBDZmq6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"a32-V72JWRAq377ByKA97w4gd2OgsG4\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 2610,
    "path": "../public/_nuxt/BbBDZmq6.js"
  },
  "/_nuxt/BbSbePv_.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1c5-FDx7GBJ8zVBx/wpZv5yq0F651o0\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 453,
    "path": "../public/_nuxt/BbSbePv_.js"
  },
  "/_nuxt/BbwNpJlj.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"8dc1-AUGiiPv2SfFLhZ/JV1kagWES56s\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 36289,
    "path": "../public/_nuxt/BbwNpJlj.js"
  },
  "/_nuxt/BcD7Klt7.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2f3-UxDwe+jDgPsIiUVVyHMmUAnLAnI\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 755,
    "path": "../public/_nuxt/BcD7Klt7.js"
  },
  "/_nuxt/Bd308Ut6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"134-/bxmppTKTFgFYanZ8FOpff0aSes\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 308,
    "path": "../public/_nuxt/Bd308Ut6.js"
  },
  "/_nuxt/BdQ4TPqZ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"123d7-LwC3ql2AUcbaqrG4eSAFy3z2X5Q\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 74711,
    "path": "../public/_nuxt/BdQ4TPqZ.js"
  },
  "/_nuxt/Be5itbO2.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11632-tWGdU9gmLTvQqYvQKrA/lTkGs3s\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 71218,
    "path": "../public/_nuxt/Be5itbO2.js"
  },
  "/_nuxt/Berf9BiZ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1996-w2eHl8eNOX+GA1EZ9yqoz4+BRuM\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 6550,
    "path": "../public/_nuxt/Berf9BiZ.js"
  },
  "/_nuxt/BghfE3TP.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11d-O6NfsZFLIucvW5Q1nTNREM7mm7M\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 285,
    "path": "../public/_nuxt/BghfE3TP.js"
  },
  "/_nuxt/BjmdyLme.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"57b-Nz0+oQQ4li0jElBI8OIkM791xrA\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 1403,
    "path": "../public/_nuxt/BjmdyLme.js"
  },
  "/_nuxt/Bk9RiOHF.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c33-1+jfMeCWZb/9/rPPsIQ3tqARiII\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 3123,
    "path": "../public/_nuxt/Bk9RiOHF.js"
  },
  "/_nuxt/BktXwn4d.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c18-pwGktzhMPMemAV4BXKqHW11pGU0\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 3096,
    "path": "../public/_nuxt/BktXwn4d.js"
  },
  "/_nuxt/BoyTJOO7.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"164a-biH/cH8h4EaGbEUPNYClJyLb2K4\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 5706,
    "path": "../public/_nuxt/BoyTJOO7.js"
  },
  "/_nuxt/BpT2DfWX.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"d9-DVTKT2JcsROUOzm99/IciQXyS0Q\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 217,
    "path": "../public/_nuxt/BpT2DfWX.js"
  },
  "/_nuxt/BqRb64FH.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"39b-DdH3ud4mjGYtiindLsbNM1ebaq0\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 923,
    "path": "../public/_nuxt/BqRb64FH.js"
  },
  "/_nuxt/BrqFm5Y-.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11e5-81XsoSsrdO3sr/u7cgT2xS+i6K8\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 4581,
    "path": "../public/_nuxt/BrqFm5Y-.js"
  },
  "/_nuxt/BsrfGeMc.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1223f-oui/GG8w6RE9Iewh8uG4qaKFIYE\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 74303,
    "path": "../public/_nuxt/BsrfGeMc.js"
  },
  "/_nuxt/BuNbMyK6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1ab8-8XQImw0xT5x9aoTODL6i1eODtj0\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 6840,
    "path": "../public/_nuxt/BuNbMyK6.js"
  },
  "/_nuxt/Bud6H6G8.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"a37-z78ihvHmQ2S+BWI1E6Y6y6bqzZg\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 2615,
    "path": "../public/_nuxt/Bud6H6G8.js"
  },
  "/_nuxt/Bueq24LW.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"a29-jBy4US5gPh0+JStstpEmTHGPI/I\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 2601,
    "path": "../public/_nuxt/Bueq24LW.js"
  },
  "/_nuxt/BuvQiibk.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"15c-hAXjjdbYES1Dj/CoRfgBLGykIqc\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 348,
    "path": "../public/_nuxt/BuvQiibk.js"
  },
  "/_nuxt/BuyPaTwS.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"981-JSNnb+aVlqq4+UhNp5XFyuER6LY\"",
    "mtime": "2025-11-14T09:22:03.366Z",
    "size": 2433,
    "path": "../public/_nuxt/BuyPaTwS.js"
  },
  "/_nuxt/Bvj36fxP.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2680-Z9oHU8nTzTFnjyykmswLhcSdDto\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 9856,
    "path": "../public/_nuxt/Bvj36fxP.js"
  },
  "/_nuxt/BvrG9P_S.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5a-oIAGDQHTBCO96uauKYXvOcxMvTk\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 90,
    "path": "../public/_nuxt/BvrG9P_S.js"
  },
  "/_nuxt/Bw4fmNEO.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1cb6-ai4rfo/ESqVTDT+t6BK9vtCOeuo\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 7350,
    "path": "../public/_nuxt/Bw4fmNEO.js"
  },
  "/_nuxt/Bx4RlH4M.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"168-Gyx/WvVdQaCYtr9mitJaD5+W+GI\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 360,
    "path": "../public/_nuxt/Bx4RlH4M.js"
  },
  "/_nuxt/BxcCKhjp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"dfd-kWsWDNNGU4Q8gNtx/qtKpQFa5Mc\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 3581,
    "path": "../public/_nuxt/BxcCKhjp.js"
  },
  "/_nuxt/Bzj1GlSb.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9c1-Bai9C4PZdABOpwHky7M5pSWkl/g\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 2497,
    "path": "../public/_nuxt/Bzj1GlSb.js"
  },
  "/_nuxt/C-e8GtUp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5dd-NRJDgvSkovkRUr/vPCURXJT2d7I\"",
    "mtime": "2025-11-14T09:22:03.367Z",
    "size": 1501,
    "path": "../public/_nuxt/C-e8GtUp.js"
  },
  "/_nuxt/C-qry8D2.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-OlVlNIriL5j0nfn/+xBudLx/b9U\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/C-qry8D2.js"
  },
  "/_nuxt/C00RwhVh.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"632-LhEroBl11GgjcZ5SBQPE5KleZyc\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 1586,
    "path": "../public/_nuxt/C00RwhVh.js"
  },
  "/_nuxt/C0RMVnBu.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-ct/aRLOqnaVJwIxK/dxchNmPeEI\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/C0RMVnBu.js"
  },
  "/_nuxt/C0dqjJ9f.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1307d-zN882b5v7sW14at4DHqAbnaHF20\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 77949,
    "path": "../public/_nuxt/C0dqjJ9f.js"
  },
  "/_nuxt/C0m_ozgW.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-qcLwSdXJXXF7wJaX2yH0HkNMdJE\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/C0m_ozgW.js"
  },
  "/_nuxt/C1EXOppN.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1098-lN3OTvwCNsOi53kjFkwVnFJkwA4\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 4248,
    "path": "../public/_nuxt/C1EXOppN.js"
  },
  "/_nuxt/C3WM_J7A.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11e39-eQZb7LHix7/MZbJgtRjCDAEmhlE\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 73273,
    "path": "../public/_nuxt/C3WM_J7A.js"
  },
  "/_nuxt/C50WwavR.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11c43-9yglfd4TvrVDZNXcKLkZtOSsS+M\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 72771,
    "path": "../public/_nuxt/C50WwavR.js"
  },
  "/_nuxt/C66S8nZ4.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c3f-CApnfeKFEBo1l47uuvl2lSRaO7w\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 3135,
    "path": "../public/_nuxt/C66S8nZ4.js"
  },
  "/_nuxt/C6LiOFqs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"12f1d-JuRxaeY0g+izV01+3eqO5Mb96Nw\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 77597,
    "path": "../public/_nuxt/C6LiOFqs.js"
  },
  "/_nuxt/C8mfJt9U.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"355-zWo4d10QfzRAPuiYByb8hH4l0XE\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 853,
    "path": "../public/_nuxt/C8mfJt9U.js"
  },
  "/_nuxt/C9LUbtwK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"266-miMg3uJV98/NAIE5OF0npYQv7qg\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 614,
    "path": "../public/_nuxt/C9LUbtwK.js"
  },
  "/_nuxt/C9mkGEnp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"27a-uB8bIjOmUepk6Wl82kHWvlFJrC8\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 634,
    "path": "../public/_nuxt/C9mkGEnp.js"
  },
  "/_nuxt/C9xo5q-k.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-Bf5vBkM7Hy7PveXo3DV1KW6yTSU\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/C9xo5q-k.js"
  },
  "/_nuxt/CAYxJdhJ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-bNNtkIjuCPeBSE70GvOwwdH/d9k\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/CAYxJdhJ.js"
  },
  "/_nuxt/CBV7v0Pd.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"dfc-qqvOreSBVKl6pUIHnkmGgBXNQQk\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 3580,
    "path": "../public/_nuxt/CBV7v0Pd.js"
  },
  "/_nuxt/CDDHLbrL.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"19c5-7wxkzmr4S2G6DjqXw+XPqftbEPw\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 6597,
    "path": "../public/_nuxt/CDDHLbrL.js"
  },
  "/_nuxt/CDj-lC-L.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4302-jhs4XiJegNe7QU0uYdbv+3811VE\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 17154,
    "path": "../public/_nuxt/CDj-lC-L.js"
  },
  "/_nuxt/CElao9fl.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1a8-50rmf61RQXBzMk7jMM9nUo4EUs0\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 424,
    "path": "../public/_nuxt/CElao9fl.js"
  },
  "/_nuxt/CEoi_Mb5.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-4ncpnVbHeXluzfjAWdT/YyqzZJs\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/CEoi_Mb5.js"
  },
  "/_nuxt/CFQCC_Ee.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c6-73l3SqlqpgWHUYk6LjRsXa4CX0M\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 198,
    "path": "../public/_nuxt/CFQCC_Ee.js"
  },
  "/_nuxt/CGMxyz9z.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c8e-5RxvcggpOSCBOp6w2/n4nSZbpvE\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 3214,
    "path": "../public/_nuxt/CGMxyz9z.js"
  },
  "/_nuxt/CH4bG6Bi.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"f91a-OCx4aNFZjmVHYccVCM5ELP1zQRk\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 63770,
    "path": "../public/_nuxt/CH4bG6Bi.js"
  },
  "/_nuxt/CHJfZnmp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"770-bGAFIMratFpTcMlnd/7mND+sMng\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 1904,
    "path": "../public/_nuxt/CHJfZnmp.js"
  },
  "/_nuxt/CIxs9bcY.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"f07-EYfPDp2vFWyqKmXg8Eo8znenwvA\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 3847,
    "path": "../public/_nuxt/CIxs9bcY.js"
  },
  "/_nuxt/CKTxAY4J.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1306f-WSRydToopCrX5/ekpxiyzpJ6k2A\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 77935,
    "path": "../public/_nuxt/CKTxAY4J.js"
  },
  "/_nuxt/CL2m7tD6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11c-mKHlNRrn8j+UfCDvdLUfRmSSgbE\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 284,
    "path": "../public/_nuxt/CL2m7tD6.js"
  },
  "/_nuxt/CMDJKfAJ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-RSneG8KpxAGqHGL8n5JW4yqFGxI\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 477,
    "path": "../public/_nuxt/CMDJKfAJ.js"
  },
  "/_nuxt/CMGAleMS.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"81-VNwioYt3SO1q3mFSLDkFGeV+TZ0\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 129,
    "path": "../public/_nuxt/CMGAleMS.js"
  },
  "/_nuxt/CMT-rOGQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"28e6-n9viqN6kbAuCtLYpUcT1+/Lh6tc\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 10470,
    "path": "../public/_nuxt/CMT-rOGQ.js"
  },
  "/_nuxt/CQ-rkFKb.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5b00-3QD9Ey5wRjjb5XnbE+WzDxXzPjk\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 23296,
    "path": "../public/_nuxt/CQ-rkFKb.js"
  },
  "/_nuxt/CQJ-XsBF.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1e9-BMw2NPH0lgn7sX6dabcPxSOZR4w\"",
    "mtime": "2025-11-14T09:22:03.368Z",
    "size": 489,
    "path": "../public/_nuxt/CQJ-XsBF.js"
  },
  "/_nuxt/CQJsZITD.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"57-bzcXB12MRshtcFL/YGWgMP26MJ4\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 87,
    "path": "../public/_nuxt/CQJsZITD.js"
  },
  "/_nuxt/CRsZXLzb.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3a62-KtfYlvozTv/ECcna4ybRg5jUUps\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 14946,
    "path": "../public/_nuxt/CRsZXLzb.js"
  },
  "/_nuxt/CSeatf3p.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"88-4OPTn90Xs7GIfCOhlbZAcQ4aj3I\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 136,
    "path": "../public/_nuxt/CSeatf3p.js"
  },
  "/_nuxt/CVFDo4Xs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c4c-ZnpVuu/tDe+wa6dEjB7Cn0kJLWA\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 3148,
    "path": "../public/_nuxt/CVFDo4Xs.js"
  },
  "/_nuxt/CX6eJpRL.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"395-Lq9aQ4BoizEUlu63AdxmKeuiZEY\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 917,
    "path": "../public/_nuxt/CX6eJpRL.js"
  },
  "/_nuxt/CX7ndQtY.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"192c-UURXyZ30xyAgpwR4TY9lv91flPs\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 6444,
    "path": "../public/_nuxt/CX7ndQtY.js"
  },
  "/_nuxt/CXn91sPa.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"250-T6gwsLg40U+WaDsqIKlII6fWQtY\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 592,
    "path": "../public/_nuxt/CXn91sPa.js"
  },
  "/_nuxt/CY0SDx2B.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1262f-Tvj+zOy8ofqokwsHjLKfBxNUFnU\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 75311,
    "path": "../public/_nuxt/CY0SDx2B.js"
  },
  "/_nuxt/CYnynMOF.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-dAe5OE+iQJ3ebAb72JPv+5Ji9sw\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 477,
    "path": "../public/_nuxt/CYnynMOF.js"
  },
  "/_nuxt/CYzM9Ef0.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1117a-hqdEzibU5BUJN3Uhq3WNLu/+OIc\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 70010,
    "path": "../public/_nuxt/CYzM9Ef0.js"
  },
  "/_nuxt/CZBZIikd.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"114fa-9yQEEVYQvdX+yW6FzcBsi1FheYQ\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 70906,
    "path": "../public/_nuxt/CZBZIikd.js"
  },
  "/_nuxt/CZc_acLE.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"10c21-sXT4PJ0LfLCaG8AgHlJZImZHBrc\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 68641,
    "path": "../public/_nuxt/CZc_acLE.js"
  },
  "/_nuxt/C_2h9rvB.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11e32-AgwSdVJRm2drEDLNbTnx59bTtrE\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 73266,
    "path": "../public/_nuxt/C_2h9rvB.js"
  },
  "/_nuxt/C_D2uFY-.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11028-La1vBzsV5hL7N19t7KRzr8g/Nvc\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 69672,
    "path": "../public/_nuxt/C_D2uFY-.js"
  },
  "/_nuxt/CbUty4vU.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"173d-GXb/hxnAySNZysW175mkBE3uwN8\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 5949,
    "path": "../public/_nuxt/CbUty4vU.js"
  },
  "/_nuxt/Cc6c4FRB.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13fa-aemPMSVWwimhxVXaeXv4xh75n1o\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 5114,
    "path": "../public/_nuxt/Cc6c4FRB.js"
  },
  "/_nuxt/CcGRVrKn.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5e9-hi2F26gn2fb1rami+Uh27uSaMMs\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 1513,
    "path": "../public/_nuxt/CcGRVrKn.js"
  },
  "/_nuxt/CfOt5p-n.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"101ae-cgkc5tKuv/nBg8iUzFIfk+VTrUM\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 65966,
    "path": "../public/_nuxt/CfOt5p-n.js"
  },
  "/_nuxt/CfYZvAXi.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"54d-mHWgZ95gVaUmtjyNH4xDrQTINr4\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 1357,
    "path": "../public/_nuxt/CfYZvAXi.js"
  },
  "/_nuxt/CgNczGOc.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-g/T30xMslnfpWgOX6GWC1aNz2bQ\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 477,
    "path": "../public/_nuxt/CgNczGOc.js"
  },
  "/_nuxt/CgZxAEba.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"276d-fGp/hW+W8XiYGT3NLWG/cze1oB8\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 10093,
    "path": "../public/_nuxt/CgZxAEba.js"
  },
  "/_nuxt/ChwEl08B.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-kp7Va2modjxuleJhHl30qzxfUmM\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 477,
    "path": "../public/_nuxt/ChwEl08B.js"
  },
  "/_nuxt/CkOHOOmA.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1361-QXrmogJvD3HTvGH/B456WziBKYA\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 4961,
    "path": "../public/_nuxt/CkOHOOmA.js"
  },
  "/_nuxt/CnDY8nbm.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"6e-o6XZ23O4FNPil5qKPpnDoG2oiJQ\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 110,
    "path": "../public/_nuxt/CnDY8nbm.js"
  },
  "/_nuxt/CnJjWgsA.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"70f-l6OVCEzhfi8pU0faQUjpvSP4GgU\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 1807,
    "path": "../public/_nuxt/CnJjWgsA.js"
  },
  "/_nuxt/Cofe4nYF.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"d3e-Usz3wpNopFWH2AZY4MLwWBopsGo\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 3390,
    "path": "../public/_nuxt/Cofe4nYF.js"
  },
  "/_nuxt/CpFjl2v1.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1647-ex4Ru16mtY/Guh6SFsxhh5bjoM4\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 5703,
    "path": "../public/_nuxt/CpFjl2v1.js"
  },
  "/_nuxt/CqGpLFFw.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1653-B1IHJzwaOlmfZae6d1aLeq2MXvY\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 5715,
    "path": "../public/_nuxt/CqGpLFFw.js"
  },
  "/_nuxt/CqkleIqs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"74-rkGgBigev8deug6izmnSDn2Z1l0\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 116,
    "path": "../public/_nuxt/CqkleIqs.js"
  },
  "/_nuxt/CrudTable.CeOIUZSo.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"43-OoeUuoyHru7GGDalBmLEt9VAn/8\"",
    "mtime": "2025-11-14T09:22:03.369Z",
    "size": 67,
    "path": "../public/_nuxt/CrudTable.CeOIUZSo.css"
  },
  "/_nuxt/CsjMHnud.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"14f0-2bbB3HECE6a3Wgb7I3G2oo/5Zm8\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 5360,
    "path": "../public/_nuxt/CsjMHnud.js"
  },
  "/_nuxt/CtZPxPWc.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"265-WQt3J1IRoEchp484InH7ztZYMh0\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 613,
    "path": "../public/_nuxt/CtZPxPWc.js"
  },
  "/_nuxt/CuMPyiF7.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1a135-fKY+m+3etlJHUWNGOvBtd9TwWiQ\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 106805,
    "path": "../public/_nuxt/CuMPyiF7.js"
  },
  "/_nuxt/CunAd0v7.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-Jn/OnoG9IwG3Oq5BZy510wJ98ZQ\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 477,
    "path": "../public/_nuxt/CunAd0v7.js"
  },
  "/_nuxt/Cv8w_oqK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"149b-v0BmT58JBeXEO3ZnXENePcX58vw\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 5275,
    "path": "../public/_nuxt/Cv8w_oqK.js"
  },
  "/_nuxt/CvPerM7N.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-uxfXU20gPMHZyZ9RgYV3MDD54X0\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 477,
    "path": "../public/_nuxt/CvPerM7N.js"
  },
  "/_nuxt/Cw5X-kAn.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"32d-QuFxI1fzhltEr0xzM+Sr+NJYLQ0\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 813,
    "path": "../public/_nuxt/Cw5X-kAn.js"
  },
  "/_nuxt/CwJ-Y2Ds.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"120a2-SZG2Tm2S4+v/67//U/kjuNUrP6s\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 73890,
    "path": "../public/_nuxt/CwJ-Y2Ds.js"
  },
  "/_nuxt/CwZcFf4g.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"560-LoeJuF9jyQNsK/TTC14MUjgTJew\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 1376,
    "path": "../public/_nuxt/CwZcFf4g.js"
  },
  "/_nuxt/CwtvwXb3.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1680-MhxKhl0cqBehbxCvHTE7egTM5mo\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 5760,
    "path": "../public/_nuxt/CwtvwXb3.js"
  },
  "/_nuxt/CwxacXWx.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"10cfa-lYo89+o7JS1AjQVai7ogq034qEI\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 68858,
    "path": "../public/_nuxt/CwxacXWx.js"
  },
  "/_nuxt/CyHKs2b7.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-Tqc+xPTug5jVg8vASIdhIRIvya8\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 477,
    "path": "../public/_nuxt/CyHKs2b7.js"
  },
  "/_nuxt/D-5jOdX2.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"49b-4eH3Ay0GdoUfV/DfSLGmdm1Sn9A\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 1179,
    "path": "../public/_nuxt/D-5jOdX2.js"
  },
  "/_nuxt/D-Jm6tRQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"21e8-Z4405M32pYAghwGuQAzfVpswdcM\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 8680,
    "path": "../public/_nuxt/D-Jm6tRQ.js"
  },
  "/_nuxt/D-Ohyl-_.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"53ce-ZfqP+Wf9YgiCyO1a9YWCmZLnhEw\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 21454,
    "path": "../public/_nuxt/D-Ohyl-_.js"
  },
  "/_nuxt/D1S_6YEK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11454-OI+DauaW6wTV+cBvSLT3mKQPJXo\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 70740,
    "path": "../public/_nuxt/D1S_6YEK.js"
  },
  "/_nuxt/D3ZVEQFu.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"94a3-qPutOc6qVKYauUFcVkAzjghFcMQ\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 38051,
    "path": "../public/_nuxt/D3ZVEQFu.js"
  },
  "/_nuxt/D3Zz0vuW.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"d05-7mWI5nbaKrpDRrOrYnEnP/5mRe8\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 3333,
    "path": "../public/_nuxt/D3Zz0vuW.js"
  },
  "/_nuxt/D3hboCUu.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1d4a-mpFShCu3JPkIXjnh3d803EFfz5w\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 7498,
    "path": "../public/_nuxt/D3hboCUu.js"
  },
  "/_nuxt/D3xyJihK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4ba4-IX+wsJCzvlRWrqhdz5/+W65ymTk\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 19364,
    "path": "../public/_nuxt/D3xyJihK.js"
  },
  "/_nuxt/D5awXT9J.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"61d-4FJaCKjtt0Q8DIikNScZir4xlKQ\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 1565,
    "path": "../public/_nuxt/D5awXT9J.js"
  },
  "/_nuxt/D5wXrMlN.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3e52-hUnTJ0XVSLDhuiqt8+aKEHw4gFw\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 15954,
    "path": "../public/_nuxt/D5wXrMlN.js"
  },
  "/_nuxt/D6ExiaPG.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"10916-BZnGQohPcKllH/TsClcwpPQYh1Y\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 67862,
    "path": "../public/_nuxt/D6ExiaPG.js"
  },
  "/_nuxt/D8RHKT85.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1ad6-/ZTAyQYDV8RpnfkbHOk3zbelp2s\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 6870,
    "path": "../public/_nuxt/D8RHKT85.js"
  },
  "/_nuxt/D8WSV-y4.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"273-rT0Lz8YXUXbBN5Axi8XWE5vluQE\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 627,
    "path": "../public/_nuxt/D8WSV-y4.js"
  },
  "/_nuxt/D8_5mNMK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13e9-QxHGjPMCTVnYS77S6kMocUq8gB0\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 5097,
    "path": "../public/_nuxt/D8_5mNMK.js"
  },
  "/_nuxt/D8mRw_c6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-V5oCqFreZPQdxOKbQ1JjH/cYGn4\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 477,
    "path": "../public/_nuxt/D8mRw_c6.js"
  },
  "/_nuxt/D94u8Au2.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"72515-y3doVX2wTDclyA+t++QWwfjCSLE\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 468245,
    "path": "../public/_nuxt/D94u8Au2.js"
  },
  "/_nuxt/D9_qOLj4.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3e6f-QBjA3ebJmLNGQvcdKuXFvhdkl54\"",
    "mtime": "2025-11-14T09:22:03.370Z",
    "size": 15983,
    "path": "../public/_nuxt/D9_qOLj4.js"
  },
  "/_nuxt/D9olWrrf.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"a365-yB2U/2a99RFM9ma/9FtuyBSb0XQ\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 41829,
    "path": "../public/_nuxt/D9olWrrf.js"
  },
  "/_nuxt/DADsPaIV.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2cdb-mcIZa6FRpA1A/luWAVTr6mByAYQ\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 11483,
    "path": "../public/_nuxt/DADsPaIV.js"
  },
  "/_nuxt/DAqGFipT.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2887-7y+btGmAmZ9mixc6fMqW/c/jfec\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 10375,
    "path": "../public/_nuxt/DAqGFipT.js"
  },
  "/_nuxt/DBtxcOFp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"f18-E28rDcoAlaSP2ubkK+ke2V9RUO8\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 3864,
    "path": "../public/_nuxt/DBtxcOFp.js"
  },
  "/_nuxt/DC8Ael1x.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"fa-S3ZkN9GmFBUt2feMUdybjcg/8iw\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 250,
    "path": "../public/_nuxt/DC8Ael1x.js"
  },
  "/_nuxt/DCvL6BNI.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5e-QB2Nkey8C6MnBb332KNQ9bDTVlo\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 94,
    "path": "../public/_nuxt/DCvL6BNI.js"
  },
  "/_nuxt/DCwZ8wPP.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"952-lTkX5AMDFfDL76nRWOEx+oFVL2Y\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 2386,
    "path": "../public/_nuxt/DCwZ8wPP.js"
  },
  "/_nuxt/DDaC3Jc-.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-HfvFEUOEjvwdqbpgyKGL3v0MySw\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 477,
    "path": "../public/_nuxt/DDaC3Jc-.js"
  },
  "/_nuxt/DEA28_Qh.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2136-ycClUPExvTlX2fRc9wLdA4iBpbM\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 8502,
    "path": "../public/_nuxt/DEA28_Qh.js"
  },
  "/_nuxt/DGB98M4k.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"45f8-Ycc91TYg/NDt+YOnS5prOTwlObk\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 17912,
    "path": "../public/_nuxt/DGB98M4k.js"
  },
  "/_nuxt/DGpDXulQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2447-Kc2pVGoLtrL3IUoElQba9dLc+0k\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 9287,
    "path": "../public/_nuxt/DGpDXulQ.js"
  },
  "/_nuxt/DHmrR_u6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c8b-ksgflahVoCLGwjFIzmnicBlE35E\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 3211,
    "path": "../public/_nuxt/DHmrR_u6.js"
  },
  "/_nuxt/DKii_rvm.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-DCNocahwrgcmImRSmOdiHvosuMc\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 477,
    "path": "../public/_nuxt/DKii_rvm.js"
  },
  "/_nuxt/DL-TWf04.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"141-zMEl337o6GKDxQAFFotpPGZ/VgY\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 321,
    "path": "../public/_nuxt/DL-TWf04.js"
  },
  "/_nuxt/DLX5UKJK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2374-0aoRuSYkOw9YCEZKJBEA1VdHTvo\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 9076,
    "path": "../public/_nuxt/DLX5UKJK.js"
  },
  "/_nuxt/DNTYm6kx.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"112-yjk52yTMo0yUiovOZxr9bKp5oqQ\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 274,
    "path": "../public/_nuxt/DNTYm6kx.js"
  },
  "/_nuxt/DNXxr0UL.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1349-Q7l1oFibyuLb8p2CXsUJrJvEEWY\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 4937,
    "path": "../public/_nuxt/DNXxr0UL.js"
  },
  "/_nuxt/DNaogT1M.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1f6-4gEKl3O5k7whnJmBSgXZXViSXdM\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 502,
    "path": "../public/_nuxt/DNaogT1M.js"
  },
  "/_nuxt/DNbQ3O3V.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"103b6-cpDZJsJJURhGpLCUehFcQd6TXeA\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 66486,
    "path": "../public/_nuxt/DNbQ3O3V.js"
  },
  "/_nuxt/DO7pgL3T.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1f1e0-XU3EkCKPNgqKBNtHLVOd3QMastI\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 127456,
    "path": "../public/_nuxt/DO7pgL3T.js"
  },
  "/_nuxt/DPjxjYxq.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4633-E8W0juczEqFomDd/JKmS6Rjw4fw\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 17971,
    "path": "../public/_nuxt/DPjxjYxq.js"
  },
  "/_nuxt/DQukkPHI.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-Bfcn1RvRPJOnjOeQ6Py9FYLXyY0\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 477,
    "path": "../public/_nuxt/DQukkPHI.js"
  },
  "/_nuxt/DR6f4bp1.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"10ac-HmqC6elljqa8bFmRIzo0KSjeb6Y\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 4268,
    "path": "../public/_nuxt/DR6f4bp1.js"
  },
  "/_nuxt/DSBtS9Gg.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-/o/FuLlHBhp6gZMq3tPWv1DfcrU\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 477,
    "path": "../public/_nuxt/DSBtS9Gg.js"
  },
  "/_nuxt/DTFF5UWs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1248c-fv8gXBB2rzaodQT+6QRuNjbp/HA\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 74892,
    "path": "../public/_nuxt/DTFF5UWs.js"
  },
  "/_nuxt/DTguV8S9.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"be-mdg8dQ0YsBriLhwMExL9x/pDXH8\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 190,
    "path": "../public/_nuxt/DTguV8S9.js"
  },
  "/_nuxt/DUpUOLLM.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-05CoIfEnVMtiVC/dgayrmnS2Z4o\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 477,
    "path": "../public/_nuxt/DUpUOLLM.js"
  },
  "/_nuxt/DUr39kAK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"d20-fQT3AWQ+ivKRysbh11HT6ag2lbQ\"",
    "mtime": "2025-11-14T09:22:03.371Z",
    "size": 3360,
    "path": "../public/_nuxt/DUr39kAK.js"
  },
  "/_nuxt/DVSs7lJe.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"ea6-ofTLxvoDLOxmSCFC0/wsTnGtxzg\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 3750,
    "path": "../public/_nuxt/DVSs7lJe.js"
  },
  "/_nuxt/DWQQFH0f.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-xYFd5AEQUFFci73nRIJ4tHsROvI\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 477,
    "path": "../public/_nuxt/DWQQFH0f.js"
  },
  "/_nuxt/DX1klFKQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"a5a-a1m1LOmlfKi0aRoVCnokhIQwWDQ\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 2650,
    "path": "../public/_nuxt/DX1klFKQ.js"
  },
  "/_nuxt/DX8eFt2g.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-tw0rYfwoRhaluS51qb0AdX6wkMk\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 477,
    "path": "../public/_nuxt/DX8eFt2g.js"
  },
  "/_nuxt/DX94Mpr9.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1379-1b1Elg9HIf7F7BlAFufy+n2NNH4\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 4985,
    "path": "../public/_nuxt/DX94Mpr9.js"
  },
  "/_nuxt/DXTkxTkx.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-J7e2UOLJCbhRAbjuZa9ULn6yqkM\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 477,
    "path": "../public/_nuxt/DXTkxTkx.js"
  },
  "/_nuxt/DXnGurpj.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"465-3jRP22P2ewO4C+5s74SsIz2h18I\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 1125,
    "path": "../public/_nuxt/DXnGurpj.js"
  },
  "/_nuxt/DYM2xP96.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"118d1-v4pCaOaGVL6fGuGNNcyilzwoQDY\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 71889,
    "path": "../public/_nuxt/DYM2xP96.js"
  },
  "/_nuxt/DZqcgL3S.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4587-+cZWH/E0jklWdZDS7hOUwryxJYg\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 17799,
    "path": "../public/_nuxt/DZqcgL3S.js"
  },
  "/_nuxt/Da1EmEsm.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-X7ksJopb0U5fKaBhpuGVOigUnqY\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 477,
    "path": "../public/_nuxt/Da1EmEsm.js"
  },
  "/_nuxt/DaOi8tSX.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"15ba-CCo/8y7O31QOfoRNrgSyICC3XJs\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 5562,
    "path": "../public/_nuxt/DaOi8tSX.js"
  },
  "/_nuxt/DeN2sE3s.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"b21-pJe4Hi2HmMb6GvVDc3sI5fwPXm0\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 2849,
    "path": "../public/_nuxt/DeN2sE3s.js"
  },
  "/_nuxt/DelXqjSp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"200c-jkrQXBKOsg+OE/iGImAp+C37eqs\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 8204,
    "path": "../public/_nuxt/DelXqjSp.js"
  },
  "/_nuxt/DezTePF0.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"dc6-f9KW9wbfj9DEkp6optr/+IUl6+A\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 3526,
    "path": "../public/_nuxt/DezTePF0.js"
  },
  "/_nuxt/DgSn-stq.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11f6d-/JNgyOErVHQvtkjkJgBji3LK4ms\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 73581,
    "path": "../public/_nuxt/DgSn-stq.js"
  },
  "/_nuxt/DgZxQMuy.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1cc7c-MzpMDpo35i+wtY+DvTemGSsrGXo\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 117884,
    "path": "../public/_nuxt/DgZxQMuy.js"
  },
  "/_nuxt/DhcSsTIT.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1b41-7EOWjTCDx2ul21UQULuHd4bD3lI\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 6977,
    "path": "../public/_nuxt/DhcSsTIT.js"
  },
  "/_nuxt/DhpjnGcG.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1022a-dVABdRhX31BH4YFDUL5oRvIE1QA\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 66090,
    "path": "../public/_nuxt/DhpjnGcG.js"
  },
  "/_nuxt/DicAFHHf.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5ad-5ASlwIIXgM82D7fXTAUPChjpCLY\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 1453,
    "path": "../public/_nuxt/DicAFHHf.js"
  },
  "/_nuxt/Djer56Nn.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c4-sPmEeRfNE659KZIVGRftEuTezL0\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 196,
    "path": "../public/_nuxt/Djer56Nn.js"
  },
  "/_nuxt/DkcJ-k9b.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2041-6DOHTq7Y/Y60SlBT57/hyzDFMfo\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 8257,
    "path": "../public/_nuxt/DkcJ-k9b.js"
  },
  "/_nuxt/DlnPTtZs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1ce0-pDmKaANpDwZXZ6+bhJw9iF7zmfI\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 7392,
    "path": "../public/_nuxt/DlnPTtZs.js"
  },
  "/_nuxt/DlwgrOtI.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"22b7-tRZgbtkzmnOGlA/Do3aQ9HZPaTs\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 8887,
    "path": "../public/_nuxt/DlwgrOtI.js"
  },
  "/_nuxt/DmniFE0M.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-FKXOC/t8vFnN4V6Z94aoX/RuH9g\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 477,
    "path": "../public/_nuxt/DmniFE0M.js"
  },
  "/_nuxt/DnbG6rbW.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1468-JhPl/zNaF/yNdVFK4hkPuSIe5JA\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 5224,
    "path": "../public/_nuxt/DnbG6rbW.js"
  },
  "/_nuxt/DooijGXU.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"112e8-KsxQ6UNfC+sTuFMzZ56VnMW8lKk\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 70376,
    "path": "../public/_nuxt/DooijGXU.js"
  },
  "/_nuxt/DoqRNS50.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"419-T5G5/mmsocSncE1fJxc+odHERyY\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 1049,
    "path": "../public/_nuxt/DoqRNS50.js"
  },
  "/_nuxt/DoytY9gA.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2943-pz7WbxtTqVkLFTlc3KP3acZpMq8\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 10563,
    "path": "../public/_nuxt/DoytY9gA.js"
  },
  "/_nuxt/Dpo6Zqq1.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c2d-BFUSMoFQPtxDw2YYzh12N+TCZR8\"",
    "mtime": "2025-11-14T09:22:03.372Z",
    "size": 3117,
    "path": "../public/_nuxt/Dpo6Zqq1.js"
  },
  "/_nuxt/Dqo2TXNH.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1fd-NtUP4+237NpGK5KxKTFWFkspkmw\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 509,
    "path": "../public/_nuxt/Dqo2TXNH.js"
  },
  "/_nuxt/DqqBjKb7.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-aN6ecEwsib5Efa6M1b0ENDUcJJM\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 477,
    "path": "../public/_nuxt/DqqBjKb7.js"
  },
  "/_nuxt/DrIVc4lk.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"15e4-jKafY7MPsPRtmadiZ+UNtoLBRJ4\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 5604,
    "path": "../public/_nuxt/DrIVc4lk.js"
  },
  "/_nuxt/Dtd4uS2y.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"602-XHDnTaAhrqCsen+AMgUh8sux0lo\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 1538,
    "path": "../public/_nuxt/Dtd4uS2y.js"
  },
  "/_nuxt/DtjBnU9f.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9c-629X0Z+cbsaOOJLsfD1FK6ocol8\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 156,
    "path": "../public/_nuxt/DtjBnU9f.js"
  },
  "/_nuxt/DvSrNVkB.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"12033-XWGXI25m+M6FBF+ngfI2k0bfylA\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 73779,
    "path": "../public/_nuxt/DvSrNVkB.js"
  },
  "/_nuxt/DvmwQN6u.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1efe-Tei07X46nF0jEVJ61v7+EKBOIe0\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 7934,
    "path": "../public/_nuxt/DvmwQN6u.js"
  },
  "/_nuxt/DvzY96yy.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4350-LzM/j/cAHOGgHcGakyjEqoQs32A\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 17232,
    "path": "../public/_nuxt/DvzY96yy.js"
  },
  "/_nuxt/Dw8OnYLf.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"8da-eDqhItxpjFulDA1kTgGzENJYbCM\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 2266,
    "path": "../public/_nuxt/Dw8OnYLf.js"
  },
  "/_nuxt/DwxUIDSs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"906-I0S5byxevpjT/e0erdEHYen5g1E\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 2310,
    "path": "../public/_nuxt/DwxUIDSs.js"
  },
  "/_nuxt/DyR1cOIE.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"308-yBE4SVTFgIoxSNza13dqTSBygFU\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 776,
    "path": "../public/_nuxt/DyR1cOIE.js"
  },
  "/_nuxt/Dz1HudxA.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"197b-nD96ib+CbVPXkT4ICCyERgyUxZo\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 6523,
    "path": "../public/_nuxt/Dz1HudxA.js"
  },
  "/_nuxt/Dz89S3Fq.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"105f-DA4Ex0mU3x6MGey9DvPYx8CsKzE\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 4191,
    "path": "../public/_nuxt/Dz89S3Fq.js"
  },
  "/_nuxt/EU3o_xlm.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3ae-8Rqd0VKm+BYtZGsboLC8KRAWvaQ\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 942,
    "path": "../public/_nuxt/EU3o_xlm.js"
  },
  "/_nuxt/Fx6pSeeb.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13ff1-ql6am0i/H10x3DRwk3PwCQkDSSY\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 81905,
    "path": "../public/_nuxt/Fx6pSeeb.js"
  },
  "/_nuxt/GHDV8C0n.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2d7d-dsxFSj6sAvyOGskuunT2kpNjhDc\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 11645,
    "path": "../public/_nuxt/GHDV8C0n.js"
  },
  "/_nuxt/HA3ZkR_G.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1c5-vJYJQ40z77zm2bQ1LP8dW9Z1B94\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 453,
    "path": "../public/_nuxt/HA3ZkR_G.js"
  },
  "/_nuxt/Hj_LnR3E.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"17f2-O45Zvj/d+H1MW7EPUMy0pU1BC/U\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 6130,
    "path": "../public/_nuxt/Hj_LnR3E.js"
  },
  "/_nuxt/IEFquJ_c.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"355f-tNcaDxmyWgmwwzjwUV1b5OOhkwc\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 13663,
    "path": "../public/_nuxt/IEFquJ_c.js"
  },
  "/_nuxt/Ia7p1OpR.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13cb6-fIkyqG6Zd6/bfaJXFDjapFan/wQ\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 81078,
    "path": "../public/_nuxt/Ia7p1OpR.js"
  },
  "/_nuxt/ImageCropper.Dw47-jjr.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"10b7-5ze7F4JM7TtCZ9PTzrCB64ahZ8I\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 4279,
    "path": "../public/_nuxt/ImageCropper.Dw47-jjr.css"
  },
  "/_nuxt/N-6XSvQX.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"95f-6LyocevfZZ6HhrntryBPo2YcOsM\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 2399,
    "path": "../public/_nuxt/N-6XSvQX.js"
  },
  "/_nuxt/N6Ej9MlG.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"bca-wHkIhfSjJjHW6gAIEWDBkJEX9lc\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 3018,
    "path": "../public/_nuxt/N6Ej9MlG.js"
  },
  "/_nuxt/NEqvLF6L.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"413-kxRDntAon7yCJ9ZYMWurgrn6wRQ\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 1043,
    "path": "../public/_nuxt/NEqvLF6L.js"
  },
  "/_nuxt/Nfg-tmTb.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"686-gyLQGZ2UYok4cnvkYjQ+BSwMXmY\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 1670,
    "path": "../public/_nuxt/Nfg-tmTb.js"
  },
  "/_nuxt/Oz1w9x5Z.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"6204-vploZlxw1bsmQnMpQXRmyfp5ivM\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 25092,
    "path": "../public/_nuxt/Oz1w9x5Z.js"
  },
  "/_nuxt/P_j0pGsM.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"7646-afIoYynmm0pP5IU+b3pfoB8JaWE\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 30278,
    "path": "../public/_nuxt/P_j0pGsM.js"
  },
  "/_nuxt/Q33NLoFs.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"4c-ELbM5WYkMLkEaQxigkZrApZILVA\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 76,
    "path": "../public/_nuxt/Q33NLoFs.js"
  },
  "/_nuxt/QueryFilterBuilder.B7OPCSwT.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"21-k8Bqv+UuLGynkAa4+bnz/va+q6U\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 33,
    "path": "../public/_nuxt/QueryFilterBuilder.B7OPCSwT.css"
  },
  "/_nuxt/RGqd7Q96.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"35f4-1QMxHFlpNcBAntL8Vv51gdsaVCY\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 13812,
    "path": "../public/_nuxt/RGqd7Q96.js"
  },
  "/_nuxt/RQ-cZqro.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"7e9-wKx4D39RpsQ9sgiMYXeHGoU76Yk\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 2025,
    "path": "../public/_nuxt/RQ-cZqro.js"
  },
  "/_nuxt/RecipeCardImage.D7wEjns0.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"fc-v/UYgLBx/QA/CPI7cAdD3xTJtUw\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 252,
    "path": "../public/_nuxt/RecipeCardImage.D7wEjns0.css"
  },
  "/_nuxt/RecipeCardMobile.DaGv57ER.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"417-S+M7ZOinDpEi8pP/tCSQ/Ze4Z64\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 1047,
    "path": "../public/_nuxt/RecipeCardMobile.DaGv57ER.css"
  },
  "/_nuxt/RecipeCardSection.CWGu24M7.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"179-s07oKrldb0u3p2Vlz0BaW1h4ZwI\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 377,
    "path": "../public/_nuxt/RecipeCardSection.CWGu24M7.css"
  },
  "/_nuxt/RecipeDialogAddToShoppingList.CNlB22lh.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"73-i/IjVg+DKZ0Izk776OoNmU0c+Go\"",
    "mtime": "2025-11-14T09:22:03.373Z",
    "size": 115,
    "path": "../public/_nuxt/RecipeDialogAddToShoppingList.CNlB22lh.css"
  },
  "/_nuxt/RecipeIngredientListItem.D-0BxQ9s.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"25f-p2CU5Rp5+Jt3984bL73ro/G8Vxs\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 607,
    "path": "../public/_nuxt/RecipeIngredientListItem.D-0BxQ9s.css"
  },
  "/_nuxt/RecipeOrganizerSelector.l4dYsoHC.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"31-gO+1AY8abHt9yfccZgx+YVgzdB4\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 49,
    "path": "../public/_nuxt/RecipeOrganizerSelector.l4dYsoHC.css"
  },
  "/_nuxt/RecipePage.Bl1XYXhO.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"2293-vAwUj4JnjzdiPvLyFY7oOEkB4nk\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 8851,
    "path": "../public/_nuxt/RecipePage.Bl1XYXhO.css"
  },
  "/_nuxt/RecipePrintView.CD6dF3PX.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"5d5-jnVFVJrytcZaGCLoE+dq8usY5D0\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 1493,
    "path": "../public/_nuxt/RecipePrintView.CD6dF3PX.css"
  },
  "/_nuxt/RecipeTimeline.C19z6k-F.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"3ee0-YiDa9w1jQg8N/eLz+GvGTP2b8uQ\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 16096,
    "path": "../public/_nuxt/RecipeTimeline.C19z6k-F.css"
  },
  "/_nuxt/RykoaQYa.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"88e-mGFgt6zjJw0XnfofdK7uhG1tnhA\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 2190,
    "path": "../public/_nuxt/RykoaQYa.js"
  },
  "/_nuxt/SXgzmQzh.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1de-X5pHJAh9jqfqfgnjTNkechRAbLU\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 478,
    "path": "../public/_nuxt/SXgzmQzh.js"
  },
  "/_nuxt/SafeMarkdown.fzWtLDK3.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"102-uAeEeC6UbEhRHZ156WRM1izZCl8\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 258,
    "path": "../public/_nuxt/SafeMarkdown.fzWtLDK3.css"
  },
  "/_nuxt/Sb_5-ZDU.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5764-agUL/1hDJWyeDEFN6+ICEfK8YnE\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 22372,
    "path": "../public/_nuxt/Sb_5-ZDU.js"
  },
  "/_nuxt/SearchFilter.WjIi3Oip.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"11d-dr+8WJcHsR1sLWbzI6CoDaVDyhE\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 285,
    "path": "../public/_nuxt/SearchFilter.WjIi3Oip.css"
  },
  "/_nuxt/TGiKtuGY.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9d2-2mW8WIVnxQoWSh2u9yIpuWZd/Uk\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 2514,
    "path": "../public/_nuxt/TGiKtuGY.js"
  },
  "/_nuxt/TgVuinvo.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3863-wR4QZUYbCUOJlL5rbUYyly4cyZk\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 14435,
    "path": "../public/_nuxt/TgVuinvo.js"
  },
  "/_nuxt/Tss4Y-pK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"563-dOzD7gfpzCTWH96WF6xzqJnehi4\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 1379,
    "path": "../public/_nuxt/Tss4Y-pK.js"
  },
  "/_nuxt/UserRegistrationForm.C7Jzt9Kj.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1b1-6P05Dz7Obnjbt6UMA7dsr4pWoe0\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 433,
    "path": "../public/_nuxt/UserRegistrationForm.C7Jzt9Kj.css"
  },
  "/_nuxt/VAlert.Cx5u1eEf.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1222-Ii0iRHwzIvrhwKO+XZqcmcHHSAk\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 4642,
    "path": "../public/_nuxt/VAlert.Cx5u1eEf.css"
  },
  "/_nuxt/VApp.5sh4-81E.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"134-hJHhXnje4cy5w9JHtFBXYUDUoYk\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 308,
    "path": "../public/_nuxt/VApp.5sh4-81E.css"
  },
  "/_nuxt/VAppBar.CtzDvqhp.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1e4-hknLGgY2bCmc7YC3WrLaJNKIFgg\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 484,
    "path": "../public/_nuxt/VAppBar.CtzDvqhp.css"
  },
  "/_nuxt/VAutocomplete.FK_0-Wol.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"9af-O2WvBdaejz5DZMgDtShHdkP25yw\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 2479,
    "path": "../public/_nuxt/VAutocomplete.FK_0-Wol.css"
  },
  "/_nuxt/VAvatar.vl36dbsm.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"d5b-yyWtHaZiBLRLHVIgTgbNrs5s07o\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 3419,
    "path": "../public/_nuxt/VAvatar.vl36dbsm.css"
  },
  "/_nuxt/VBadge.ByOuy93B.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"3f40-v9RzwS5tpxLcE79bTJ5QZZkEHZo\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 16192,
    "path": "../public/_nuxt/VBadge.ByOuy93B.css"
  },
  "/_nuxt/VBtn.CzvzxRIZ.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"5536-rtdB704CVTcK1eta6uVaJfMY5CE\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 21814,
    "path": "../public/_nuxt/VBtn.CzvzxRIZ.css"
  },
  "/_nuxt/VCard.50z-qNLo.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1a08-usgA6HDYYzeybk4lUMt3imU4hFc\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 6664,
    "path": "../public/_nuxt/VCard.50z-qNLo.css"
  },
  "/_nuxt/VCheckbox.CvH8ekHL.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"6d-0CbFad/TQeJ4x6jaztFtqpweNjY\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 109,
    "path": "../public/_nuxt/VCheckbox.CvH8ekHL.css"
  },
  "/_nuxt/VChip.Crcer8s_.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"2b3e-hTnuLxmPPGlNKA6Et3+oQGxVIW8\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 11070,
    "path": "../public/_nuxt/VChip.Crcer8s_.css"
  },
  "/_nuxt/VColorPicker.nUu9QseM.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"3ad4-znuOSinVu7GS5TImcX3bPVYh8WQ\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 15060,
    "path": "../public/_nuxt/VColorPicker.nUu9QseM.css"
  },
  "/_nuxt/VDataTable.DzOn4wdR.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"2dc3-pHs2B8vdxAldgkEc3nG8m7mWjv8\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 11715,
    "path": "../public/_nuxt/VDataTable.DzOn4wdR.css"
  },
  "/_nuxt/VDatePicker.Dm-buLTl.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1081-4zW258t/Fp3WDa8LANrNANxnMcE\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 4225,
    "path": "../public/_nuxt/VDatePicker.Dm-buLTl.css"
  },
  "/_nuxt/VDialog.Dk_v9Av4.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"9b5-wsohxC9yhR5L7K+qvtTrcKlVY2U\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 2485,
    "path": "../public/_nuxt/VDialog.Dk_v9Av4.css"
  },
  "/_nuxt/VDivider.DBONV6LQ.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"353-l66yBZqNKIX1+2kdeHhk1JCpFUM\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 851,
    "path": "../public/_nuxt/VDivider.DBONV6LQ.css"
  },
  "/_nuxt/VExpansionPanels.rBe4j0TE.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"18d3-Z3Y63XAjBXq8TpojXKS0MrSQ16E\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 6355,
    "path": "../public/_nuxt/VExpansionPanels.rBe4j0TE.css"
  },
  "/_nuxt/VField.2vW_9aLc.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"4594-CK+VOn0QZU4ZiAxwT0ocskDDDro\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 17812,
    "path": "../public/_nuxt/VField.2vW_9aLc.css"
  },
  "/_nuxt/VGrid.7zN8MVSi.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"2538-MBJDookPtBRTxNO7whtWCkkhH1g\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 9528,
    "path": "../public/_nuxt/VGrid.7zN8MVSi.css"
  },
  "/_nuxt/VInput.rqrwtjxT.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1127-CUrOBDujnfESwz4Eg8F4JgFnt0E\"",
    "mtime": "2025-11-14T09:22:03.374Z",
    "size": 4391,
    "path": "../public/_nuxt/VInput.rqrwtjxT.css"
  },
  "/_nuxt/VList.2n1KPs4p.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"876-QLfg8kduIg7mHtiJ8iemmdrFTlA\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 2166,
    "path": "../public/_nuxt/VList.2n1KPs4p.css"
  },
  "/_nuxt/VListItem.BKg2YO5l.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"325b-s23Ta601wQk8MEoKJ5/qmFpXRE0\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 12891,
    "path": "../public/_nuxt/VListItem.BKg2YO5l.css"
  },
  "/_nuxt/VMain.BRLuCwGL.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"ea7-AO2arcXJACyo+AlARWplK1v7h7Q\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 3751,
    "path": "../public/_nuxt/VMain.BRLuCwGL.css"
  },
  "/_nuxt/VMenu.ADsz2A20.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1e8-qUReA5qWmqtWpINEpqwwI/frs8c\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 488,
    "path": "../public/_nuxt/VMenu.ADsz2A20.css"
  },
  "/_nuxt/VOverlay.CFFyKv8Z.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"34d-b+t15nNmgZiKFAghKVmt0LTNBaU\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 845,
    "path": "../public/_nuxt/VOverlay.CFFyKv8Z.css"
  },
  "/_nuxt/VPicker.D-EA7pL-.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"517-y0myOjJc885RpEleC83u4BdKp90\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 1303,
    "path": "../public/_nuxt/VPicker.D-EA7pL-.css"
  },
  "/_nuxt/VSelect.C_PgXfhg.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"671-EKBN4cudE4aCmilcassnmMuT2ys\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 1649,
    "path": "../public/_nuxt/VSelect.C_PgXfhg.css"
  },
  "/_nuxt/VSelectionControl.CdaDJBAG.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"8bd-dEjTFG97wH8VA8gkMQjc5hGx8gE\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 2237,
    "path": "../public/_nuxt/VSelectionControl.CdaDJBAG.css"
  },
  "/_nuxt/VSheet.BOaw1GDg.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"2a7-zfqDAwvwv4zh7k4J31uj+r6hY6E\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 679,
    "path": "../public/_nuxt/VSheet.BOaw1GDg.css"
  },
  "/_nuxt/VSlideGroup.BsYIg1rJ.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"3c4-oEa6PKe3c2mGvey8EUkJXkJY0wQ\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 964,
    "path": "../public/_nuxt/VSlideGroup.BsYIg1rJ.css"
  },
  "/_nuxt/VSwitch.D8XUAa0O.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"1349-AvGnIXzn/qxhIPL1DyAa/yGKS9A\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 4937,
    "path": "../public/_nuxt/VSwitch.D8XUAa0O.css"
  },
  "/_nuxt/VTextarea.btQPEStR.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"5e0-iHQg3IGc4nRiBFgPRO1fkArZ3a4\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 1504,
    "path": "../public/_nuxt/VTextarea.btQPEStR.css"
  },
  "/_nuxt/VToolbar.DqxZhxt8.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"a15-qcUPupW1HpwyyJaqwKYiUUKkKf4\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 2581,
    "path": "../public/_nuxt/VToolbar.DqxZhxt8.css"
  },
  "/_nuxt/VTooltip.fl0ZvfAg.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"28c-fydliBh/Jve0qXGPtKkgToBHkLY\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 652,
    "path": "../public/_nuxt/VTooltip.fl0ZvfAg.css"
  },
  "/_nuxt/VVirtualScroll.BNcY_ygg.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"89-MwklqmaOeronE0YDW2dBQ4y4tfE\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 137,
    "path": "../public/_nuxt/VVirtualScroll.BNcY_ygg.css"
  },
  "/_nuxt/VWindowItem.fXpl8w0Y.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"da9-LKwycTXDQHaiHcK5PoL1wj85o7w\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 3497,
    "path": "../public/_nuxt/VWindowItem.fXpl8w0Y.css"
  },
  "/_nuxt/VuG9GbcK.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3fb-5vgyz9vHgVcAbQSXcR+SlfR/9JA\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 1019,
    "path": "../public/_nuxt/VuG9GbcK.js"
  },
  "/_nuxt/W-tIwFAP.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"41ed-51x9Umx75nwK12RgpZ55xTGGBIQ\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 16877,
    "path": "../public/_nuxt/W-tIwFAP.js"
  },
  "/_nuxt/W249XJwh.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-AWJIFDHYl1XgbiYcQsrcIgfkwpM\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 477,
    "path": "../public/_nuxt/W249XJwh.js"
  },
  "/_nuxt/WvA29Sbp.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1252-0JWN1maels9zuTyQQhwWSTmSwQU\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 4690,
    "path": "../public/_nuxt/WvA29Sbp.js"
  },
  "/_nuxt/XalaskvH.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"14ae-r+O71UpV/rJ7DU7guM8P/seRjYs\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 5294,
    "path": "../public/_nuxt/XalaskvH.js"
  },
  "/_nuxt/Y0IAlrHE.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"f94-KK/HLYEuoREAMPf42rTmTVmGvxQ\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 3988,
    "path": "../public/_nuxt/Y0IAlrHE.js"
  },
  "/_nuxt/Z2tnDFk9.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"102a5-I9/hIxdvE20opnrOWX2VFZy/S0s\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 66213,
    "path": "../public/_nuxt/Z2tnDFk9.js"
  },
  "/_nuxt/ZHyI8HNr.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"5848-nM3zvukTvMq/alRgFpFK02Tey5o\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 22600,
    "path": "../public/_nuxt/ZHyI8HNr.js"
  },
  "/_nuxt/Zt9ozI0c.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-HJ48ENzNf/aSDY9xYsvrrKQRbSI\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 477,
    "path": "../public/_nuxt/Zt9ozI0c.js"
  },
  "/_nuxt/_2kHfjcn.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"116b1-zO0xdUe3nIJ+3hjN8VbT3x/PI9Q\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 71345,
    "path": "../public/_nuxt/_2kHfjcn.js"
  },
  "/_nuxt/_id_.C_waJtlt.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"70-7+rLEGDZbTDyCdD7snbAUha6Cp4\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 112,
    "path": "../public/_nuxt/_id_.C_waJtlt.css"
  },
  "/_nuxt/_pBSd_wQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"13bba-2hKt/xzuegNTM570pcFDMdg6tGo\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 80826,
    "path": "../public/_nuxt/_pBSd_wQ.js"
  },
  "/_nuxt/autofocus.BtHNdAsI.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"7e0-Xj7V3RY1B/IyDT38GlFvYO/EhSQ\"",
    "mtime": "2025-11-14T09:22:03.375Z",
    "size": 2016,
    "path": "../public/_nuxt/autofocus.BtHNdAsI.css"
  },
  "/_nuxt/bPJieSd-.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"bee-L5IHMBkk6kCxQKkv533h13Akrzg\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 3054,
    "path": "../public/_nuxt/bPJieSd-.js"
  },
  "/_nuxt/backups.eqfSDEIq.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"38-VK+U0Jy+9ISPQZzR3/i/noqBZPM\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 56,
    "path": "../public/_nuxt/backups.eqfSDEIq.css"
  },
  "/_nuxt/blank.BXXCCnni.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"eae-OFDaA7eZQ9qWhNs0rpNr9yxqd5Q\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 3758,
    "path": "../public/_nuxt/blank.BXXCCnni.css"
  },
  "/_nuxt/c0C3tu9Y.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"395f-VlWQa6oB8AOchmZhVSHQZ7EDND0\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 14687,
    "path": "../public/_nuxt/c0C3tu9Y.js"
  },
  "/_nuxt/cgamdj-6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"6ed-djTtYkdbKeamw4oYUCTFlGmcXME\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 1773,
    "path": "../public/_nuxt/cgamdj-6.js"
  },
  "/_nuxt/e6y-Co5I.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"16b2-ynhwUjPdQiroMiLm1ZpeoXBuwec\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 5810,
    "path": "../public/_nuxt/e6y-Co5I.js"
  },
  "/_nuxt/eKB5BHq8.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"3db-+5r9mO2zDFbcbFBw3ngKqITsAME\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 987,
    "path": "../public/_nuxt/eKB5BHq8.js"
  },
  "/_nuxt/edit.7v7fsxst.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"91b-2AeLxOwaiLjs5SaavI/MpAFtv0w\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 2331,
    "path": "../public/_nuxt/edit.7v7fsxst.css"
  },
  "/_nuxt/entry.DBHY5DSU.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"406ba-w4HzX9OktUjFyFuc/vY8M7OwwbU\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 263866,
    "path": "../public/_nuxt/entry.DBHY5DSU.css"
  },
  "/_nuxt/error-404.DuL-z3QU.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"dca-0O1Uh22vSVDHrfWNQrle0oH17Zo\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 3530,
    "path": "../public/_nuxt/error-404.DuL-z3QU.css"
  },
  "/_nuxt/error-500.Ba4qlV26.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"75a-P7D+KDgn1YT2G5SfQvqo9DJvjEM\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 1882,
    "path": "../public/_nuxt/error-500.Ba4qlV26.css"
  },
  "/_nuxt/error.Da5JUKvS.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"7c-21gnIOHE7ebgpGW2iqbRNwJ2F0A\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 124,
    "path": "../public/_nuxt/error.Da5JUKvS.css"
  },
  "/_nuxt/g-ud41Xm.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"c6c-SEHzjs1tLZ5aAjrheyPOZ2z+asQ\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 3180,
    "path": "../public/_nuxt/g-ud41Xm.js"
  },
  "/_nuxt/g3myYh9T.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"16bb-FAeFe3O/ZBVsEDfXf5cqw1/aZZA\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 5819,
    "path": "../public/_nuxt/g3myYh9T.js"
  },
  "/_nuxt/hbiqtKID.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1ec-5Nubm7oH/oJa50ZqmbcinlClB1k\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 492,
    "path": "../public/_nuxt/hbiqtKID.js"
  },
  "/_nuxt/index.BRybATDI.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"177-14cWLZblaPcwjLf7D11eO+68p/8\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 375,
    "path": "../public/_nuxt/index.BRybATDI.css"
  },
  "/_nuxt/index.BpN7xz8k.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"45-BBLnPD7Er/2gc93HGMlPZ5L0xtw\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 69,
    "path": "../public/_nuxt/index.BpN7xz8k.css"
  },
  "/_nuxt/index.CjkcQvKm.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"112-2wl3VZLptWavKmx9gv0UgkV9h6k\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 274,
    "path": "../public/_nuxt/index.CjkcQvKm.css"
  },
  "/_nuxt/index.D12lkyFm.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"54-bW2VTv9iotthvEGYXqBN8hf6uPU\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 84,
    "path": "../public/_nuxt/index.D12lkyFm.css"
  },
  "/_nuxt/j3Fes4iD.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"136b-swz0s1XhuIHniMWFwpW31yZJlBk\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 4971,
    "path": "../public/_nuxt/j3Fes4iD.js"
  },
  "/_nuxt/k0WrJX9W.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"199a4-B9CCfw7Dnk0c508JTC8pB//FAQk\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 104868,
    "path": "../public/_nuxt/k0WrJX9W.js"
  },
  "/_nuxt/lUuKhBs1.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"10e1-mSBZj1IGF2VFPHZOZOhJJ0BtV3w\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 4321,
    "path": "../public/_nuxt/lUuKhBs1.js"
  },
  "/_nuxt/lX9bKjam.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1b3b0-1nmOuQFgW18A6NunWid+yIf4C6w\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 111536,
    "path": "../public/_nuxt/lX9bKjam.js"
  },
  "/_nuxt/lbXOhFmv.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"2c8-2jQNKCJXHgx0m3RkMN3ssWDm5yg\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 712,
    "path": "../public/_nuxt/lbXOhFmv.js"
  },
  "/_nuxt/lbk8hjKh.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"249-kBMNNLd3/HeuDPoCfSfN4upPbJQ\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 585,
    "path": "../public/_nuxt/lbk8hjKh.js"
  },
  "/_nuxt/loPGwi9r.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"11ca5-IIDeex0GKJFwi4CxLLpZcG0cBhI\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 72869,
    "path": "../public/_nuxt/loPGwi9r.js"
  },
  "/_nuxt/login.BYah3AXS.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"161-/iEgwKcFgB4RjTmcpOS7zS1pq3I\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 353,
    "path": "../public/_nuxt/login.BYah3AXS.css"
  },
  "/_nuxt/mPfpGwDb.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9df-miRaoHbx5I+7U9ohz7nAVUIUUt4\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 2527,
    "path": "../public/_nuxt/mPfpGwDb.js"
  },
  "/_nuxt/mUz1jKOx.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"cba-XYkQ1BeJiMvXoZQVMdLd9FQs29s\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 3258,
    "path": "../public/_nuxt/mUz1jKOx.js"
  },
  "/_nuxt/migrations.DE9RP2Zf.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"97f-SzHyUGXz2dodjyOwsc5HpV8EKU0\"",
    "mtime": "2025-11-14T09:22:03.376Z",
    "size": 2431,
    "path": "../public/_nuxt/migrations.DE9RP2Zf.css"
  },
  "/_nuxt/mo58i6ma.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-BptZqudoLcdrRQm/GT2fnZMhoTE\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 477,
    "path": "../public/_nuxt/mo58i6ma.js"
  },
  "/_nuxt/notifiers.rhj3JQX1.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"41-OTJLzO878PDqnsh1nA+f2tPS/rM\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 65,
    "path": "../public/_nuxt/notifiers.rhj3JQX1.css"
  },
  "/_nuxt/planner.D6FH_nbb.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"806-THCIMZQuQXg9uMMblRjjUOX2/6g\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 2054,
    "path": "../public/_nuxt/planner.D6FH_nbb.css"
  },
  "/_nuxt/pnnE18tC.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9b3-SD9ARG6LqgYDO5rjGR9JW0I/9+8\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 2483,
    "path": "../public/_nuxt/pnnE18tC.js"
  },
  "/_nuxt/qEQU6_xN.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"9b25-eAhYBvx5LJQF8GC3rytTAQLHtos\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 39717,
    "path": "../public/_nuxt/qEQU6_xN.js"
  },
  "/_nuxt/recipes.CHvMO1sG.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"27-sp/6lPa71d0p4B5Jj9UD+5dAVrM\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 39,
    "path": "../public/_nuxt/recipes.CHvMO1sG.css"
  },
  "/_nuxt/reset-password.DdcLZU4q.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"19-+38hV5m6nYCQQ9SY5n3U/VAzjus\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 25,
    "path": "../public/_nuxt/reset-password.DdcLZU4q.css"
  },
  "/_nuxt/riGGxSqQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-3rKeaAZiSyqLIWviJ4UXJTn3twM\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 477,
    "path": "../public/_nuxt/riGGxSqQ.js"
  },
  "/_nuxt/setup.yp-069GQ.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"13d5-9wThevVKOpUZBSfehXuBc6STB78\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 5077,
    "path": "../public/_nuxt/setup.yp-069GQ.css"
  },
  "/_nuxt/site-settings.y8JVZQkr.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"45-RX3fscgZh44TbZGdFia0Oj7Qyxc\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 69,
    "path": "../public/_nuxt/site-settings.y8JVZQkr.css"
  },
  "/_nuxt/t0y10jDX.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-Bil5n7IYTC4mQ2sr6vwroWHvFyI\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 477,
    "path": "../public/_nuxt/t0y10jDX.js"
  },
  "/_nuxt/tTtpAHq6.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"164d-zgsbs79zqY8cZjWfxbNFeUEj6HU\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 5709,
    "path": "../public/_nuxt/tTtpAHq6.js"
  },
  "/_nuxt/towsKq7g.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1e9-ZXZ7YFEBoa7Um/6ZvlRKRhFXvzY\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 489,
    "path": "../public/_nuxt/towsKq7g.js"
  },
  "/_nuxt/txfV05ql.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"12159-3wb0uKyzJONY6dGb7x57r6ZQ2xk\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 74073,
    "path": "../public/_nuxt/txfV05ql.js"
  },
  "/_nuxt/url.Cj5NuwHz.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"25-nLvJ4E+FmuZ3RAgvjmqg/ZQQ6Eg\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 37,
    "path": "../public/_nuxt/url.Cj5NuwHz.css"
  },
  "/_nuxt/utY1qoNN.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"b04-cb8MFOZgAVnLCTTyUQbJNokkF0s\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 2820,
    "path": "../public/_nuxt/utY1qoNN.js"
  },
  "/_nuxt/w3JThpYQ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1dd-DvfDZ34UHLzVL6eFscsXULaKuHw\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 477,
    "path": "../public/_nuxt/w3JThpYQ.js"
  },
  "/_nuxt/wWZLxEvu.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"dc6-jUL3SYmTfw0WqYxTNwohqOb6yHg\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 3526,
    "path": "../public/_nuxt/wWZLxEvu.js"
  },
  "/_nuxt/yIALMivo.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"17be-VzGiMxWXdQaXh4D+zVcAVgcJr+A\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 6078,
    "path": "../public/_nuxt/yIALMivo.js"
  },
  "/_nuxt/yZgVN5Du.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"16747-oHKuiw4psCch0Yczt6kNiGYy3AU\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 91975,
    "path": "../public/_nuxt/yZgVN5Du.js"
  },
  "/_nuxt/ycoUYLWZ.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"931-EQLVY1h3iQ4/SRRbdyxQuaobstw\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 2353,
    "path": "../public/_nuxt/ycoUYLWZ.js"
  },
  "/_nuxt/zip.DKRJ1GEl.css": {
    "type": "text/css; charset=utf-8",
    "etag": "\"3dc-lViLqy6CIFb1bfCjkYnaY+kfHAE\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 988,
    "path": "../public/_nuxt/zip.DKRJ1GEl.css"
  },
  "/_nuxt/zuqny-8T.js": {
    "type": "text/javascript; charset=utf-8",
    "etag": "\"1368-zwcGQpJP+FXfBuuo0Z12lAIYqXI\"",
    "mtime": "2025-11-14T09:22:03.377Z",
    "size": 4968,
    "path": "../public/_nuxt/zuqny-8T.js"
  },
  "/_nuxt/builds/latest.json": {
    "type": "application/json",
    "etag": "\"47-3ZTjCiFK5Lu+LhlywNap4J9pZTc\"",
    "mtime": "2025-11-14T09:22:03.236Z",
    "size": 71,
    "path": "../public/_nuxt/builds/latest.json"
  },
  "/_nuxt/builds/meta/3c9b37e7-ce63-4c35-bd26-1de57f5b352e.json": {
    "type": "application/json",
    "etag": "\"8b-yELtEB7Ea4Qdi8fjmw9gT4XniKs\"",
    "mtime": "2025-11-14T09:22:03.231Z",
    "size": 139,
    "path": "../public/_nuxt/builds/meta/3c9b37e7-ce63-4c35-bd26-1de57f5b352e.json"
  }
};

const _DRIVE_LETTER_START_RE = /^[A-Za-z]:\//;
function normalizeWindowsPath(input = "") {
  if (!input) {
    return input;
  }
  return input.replace(/\\/g, "/").replace(_DRIVE_LETTER_START_RE, (r) => r.toUpperCase());
}
const _IS_ABSOLUTE_RE = /^[/\\](?![/\\])|^[/\\]{2}(?!\.)|^[A-Za-z]:[/\\]/;
const _DRIVE_LETTER_RE = /^[A-Za-z]:$/;
function cwd() {
  if (typeof process !== "undefined" && typeof process.cwd === "function") {
    return process.cwd().replace(/\\/g, "/");
  }
  return "/";
}
const resolve = function(...arguments_) {
  arguments_ = arguments_.map((argument) => normalizeWindowsPath(argument));
  let resolvedPath = "";
  let resolvedAbsolute = false;
  for (let index = arguments_.length - 1; index >= -1 && !resolvedAbsolute; index--) {
    const path = index >= 0 ? arguments_[index] : cwd();
    if (!path || path.length === 0) {
      continue;
    }
    resolvedPath = `${path}/${resolvedPath}`;
    resolvedAbsolute = isAbsolute(path);
  }
  resolvedPath = normalizeString(resolvedPath, !resolvedAbsolute);
  if (resolvedAbsolute && !isAbsolute(resolvedPath)) {
    return `/${resolvedPath}`;
  }
  return resolvedPath.length > 0 ? resolvedPath : ".";
};
function normalizeString(path, allowAboveRoot) {
  let res = "";
  let lastSegmentLength = 0;
  let lastSlash = -1;
  let dots = 0;
  let char = null;
  for (let index = 0; index <= path.length; ++index) {
    if (index < path.length) {
      char = path[index];
    } else if (char === "/") {
      break;
    } else {
      char = "/";
    }
    if (char === "/") {
      if (lastSlash === index - 1 || dots === 1) ; else if (dots === 2) {
        if (res.length < 2 || lastSegmentLength !== 2 || res[res.length - 1] !== "." || res[res.length - 2] !== ".") {
          if (res.length > 2) {
            const lastSlashIndex = res.lastIndexOf("/");
            if (lastSlashIndex === -1) {
              res = "";
              lastSegmentLength = 0;
            } else {
              res = res.slice(0, lastSlashIndex);
              lastSegmentLength = res.length - 1 - res.lastIndexOf("/");
            }
            lastSlash = index;
            dots = 0;
            continue;
          } else if (res.length > 0) {
            res = "";
            lastSegmentLength = 0;
            lastSlash = index;
            dots = 0;
            continue;
          }
        }
        if (allowAboveRoot) {
          res += res.length > 0 ? "/.." : "..";
          lastSegmentLength = 2;
        }
      } else {
        if (res.length > 0) {
          res += `/${path.slice(lastSlash + 1, index)}`;
        } else {
          res = path.slice(lastSlash + 1, index);
        }
        lastSegmentLength = index - lastSlash - 1;
      }
      lastSlash = index;
      dots = 0;
    } else if (char === "." && dots !== -1) {
      ++dots;
    } else {
      dots = -1;
    }
  }
  return res;
}
const isAbsolute = function(p) {
  return _IS_ABSOLUTE_RE.test(p);
};
const dirname = function(p) {
  const segments = normalizeWindowsPath(p).replace(/\/$/, "").split("/").slice(0, -1);
  if (segments.length === 1 && _DRIVE_LETTER_RE.test(segments[0])) {
    segments[0] += "/";
  }
  return segments.join("/") || (isAbsolute(p) ? "/" : ".");
};

function readAsset (id) {
  const serverDir = dirname(fileURLToPath(globalThis._importMeta_.url));
  return promises.readFile(resolve(serverDir, assets[id].path))
}

const publicAssetBases = {"/_nuxt/builds/meta/":{"maxAge":31536000},"/_nuxt/builds/":{"maxAge":1},"/_fonts/":{"maxAge":31536000},"/_nuxt/":{"maxAge":31536000}};

function isPublicAssetURL(id = '') {
  if (assets[id]) {
    return true
  }
  for (const base in publicAssetBases) {
    if (id.startsWith(base)) { return true }
  }
  return false
}

function getAsset (id) {
  return assets[id]
}

const METHODS = /* @__PURE__ */ new Set(["HEAD", "GET"]);
const EncodingMap = { gzip: ".gz", br: ".br" };
const _FZ61RZ = eventHandler((event) => {
  if (event.method && !METHODS.has(event.method)) {
    return;
  }
  let id = decodePath(
    withLeadingSlash(withoutTrailingSlash(parseURL(event.path).pathname))
  );
  let asset;
  const encodingHeader = String(
    getRequestHeader(event, "accept-encoding") || ""
  );
  const encodings = [
    ...encodingHeader.split(",").map((e) => EncodingMap[e.trim()]).filter(Boolean).sort(),
    ""
  ];
  if (encodings.length > 1) {
    appendResponseHeader(event, "Vary", "Accept-Encoding");
  }
  for (const encoding of encodings) {
    for (const _id of [id + encoding, joinURL(id, "index.html" + encoding)]) {
      const _asset = getAsset(_id);
      if (_asset) {
        asset = _asset;
        id = _id;
        break;
      }
    }
  }
  if (!asset) {
    if (isPublicAssetURL(id)) {
      removeResponseHeader(event, "Cache-Control");
      throw createError$1({ statusCode: 404 });
    }
    return;
  }
  const ifNotMatch = getRequestHeader(event, "if-none-match") === asset.etag;
  if (ifNotMatch) {
    setResponseStatus(event, 304, "Not Modified");
    return "";
  }
  const ifModifiedSinceH = getRequestHeader(event, "if-modified-since");
  const mtimeDate = new Date(asset.mtime);
  if (ifModifiedSinceH && asset.mtime && new Date(ifModifiedSinceH) >= mtimeDate) {
    setResponseStatus(event, 304, "Not Modified");
    return "";
  }
  if (asset.type && !getResponseHeader(event, "Content-Type")) {
    setResponseHeader(event, "Content-Type", asset.type);
  }
  if (asset.etag && !getResponseHeader(event, "ETag")) {
    setResponseHeader(event, "ETag", asset.etag);
  }
  if (asset.mtime && !getResponseHeader(event, "Last-Modified")) {
    setResponseHeader(event, "Last-Modified", mtimeDate.toUTCString());
  }
  if (asset.encoding && !getResponseHeader(event, "Content-Encoding")) {
    setResponseHeader(event, "Content-Encoding", asset.encoding);
  }
  if (asset.size > 0 && !getResponseHeader(event, "Content-Length")) {
    setResponseHeader(event, "Content-Length", asset.size);
  }
  return readAsset(id);
});

const _SxA8c9 = defineEventHandler(() => {});

const _lazy_ASGUf2 = () => import('../routes/api/_..._.mjs');
const _lazy_IrlnEC = () => import('../routes/docs.mjs');
const _lazy_GBQUcV = () => import('../routes/openapi.json.mjs');
const _lazy_JHX0HP = () => import('../routes/renderer.mjs');

const handlers = [
  { route: '', handler: _FZ61RZ, lazy: false, middleware: true, method: undefined },
  { route: '/api/**', handler: _lazy_ASGUf2, lazy: true, middleware: false, method: undefined },
  { route: '/docs', handler: _lazy_IrlnEC, lazy: true, middleware: false, method: undefined },
  { route: '/openapi.json', handler: _lazy_GBQUcV, lazy: true, middleware: false, method: undefined },
  { route: '/__nuxt_error', handler: _lazy_JHX0HP, lazy: true, middleware: false, method: undefined },
  { route: '/__nuxt_island/**', handler: _SxA8c9, lazy: false, middleware: false, method: undefined },
  { route: '/**', handler: _lazy_JHX0HP, lazy: true, middleware: false, method: undefined }
];

function createNitroApp() {
  const config = useRuntimeConfig();
  const hooks = createHooks();
  const captureError = (error, context = {}) => {
    const promise = hooks.callHookParallel("error", error, context).catch((error_) => {
      console.error("Error while capturing another error", error_);
    });
    if (context.event && isEvent(context.event)) {
      const errors = context.event.context.nitro?.errors;
      if (errors) {
        errors.push({ error, context });
      }
      if (context.event.waitUntil) {
        context.event.waitUntil(promise);
      }
    }
  };
  const h3App = createApp({
    debug: destr(false),
    onError: (error, event) => {
      captureError(error, { event, tags: ["request"] });
      return errorHandler(error, event);
    },
    onRequest: async (event) => {
      event.context.nitro = event.context.nitro || { errors: [] };
      const fetchContext = event.node.req?.__unenv__;
      if (fetchContext?._platform) {
        event.context = {
          _platform: fetchContext?._platform,
          // #3335
          ...fetchContext._platform,
          ...event.context
        };
      }
      if (!event.context.waitUntil && fetchContext?.waitUntil) {
        event.context.waitUntil = fetchContext.waitUntil;
      }
      event.fetch = (req, init) => fetchWithEvent(event, req, init, { fetch: localFetch });
      event.$fetch = (req, init) => fetchWithEvent(event, req, init, {
        fetch: $fetch
      });
      event.waitUntil = (promise) => {
        if (!event.context.nitro._waitUntilPromises) {
          event.context.nitro._waitUntilPromises = [];
        }
        event.context.nitro._waitUntilPromises.push(promise);
        if (event.context.waitUntil) {
          event.context.waitUntil(promise);
        }
      };
      event.captureError = (error, context) => {
        captureError(error, { event, ...context });
      };
      await nitroApp$1.hooks.callHook("request", event).catch((error) => {
        captureError(error, { event, tags: ["request"] });
      });
    },
    onBeforeResponse: async (event, response) => {
      await nitroApp$1.hooks.callHook("beforeResponse", event, response).catch((error) => {
        captureError(error, { event, tags: ["request", "response"] });
      });
    },
    onAfterResponse: async (event, response) => {
      await nitroApp$1.hooks.callHook("afterResponse", event, response).catch((error) => {
        captureError(error, { event, tags: ["request", "response"] });
      });
    }
  });
  const router = createRouter({
    preemptive: true
  });
  const nodeHandler = toNodeListener(h3App);
  const localCall = (aRequest) => b(
    nodeHandler,
    aRequest
  );
  const localFetch = (input, init) => {
    if (!input.toString().startsWith("/")) {
      return globalThis.fetch(input, init);
    }
    return C(
      nodeHandler,
      input,
      init
    ).then((response) => normalizeFetchResponse(response));
  };
  const $fetch = createFetch({
    fetch: localFetch,
    Headers: Headers$1,
    defaults: { baseURL: config.app.baseURL }
  });
  globalThis.$fetch = $fetch;
  h3App.use(createRouteRulesHandler({ localFetch }));
  for (const h of handlers) {
    let handler = h.lazy ? lazyEventHandler(h.handler) : h.handler;
    if (h.middleware || !h.route) {
      const middlewareBase = (config.app.baseURL + (h.route || "/")).replace(
        /\/+/g,
        "/"
      );
      h3App.use(middlewareBase, handler);
    } else {
      const routeRules = getRouteRulesForPath(
        h.route.replace(/:\w+|\*\*/g, "_")
      );
      if (routeRules.cache) {
        handler = cachedEventHandler(handler, {
          group: "nitro/routes",
          ...routeRules.cache
        });
      }
      router.use(h.route, handler, h.method);
    }
  }
  h3App.use(config.app.baseURL, router.handler);
  const app = {
    hooks,
    h3App,
    router,
    localCall,
    localFetch,
    captureError
  };
  return app;
}
function runNitroPlugins(nitroApp2) {
  for (const plugin of plugins) {
    try {
      plugin(nitroApp2);
    } catch (error) {
      nitroApp2.captureError(error, { tags: ["plugin"] });
      throw error;
    }
  }
}
const nitroApp$1 = createNitroApp();
function useNitroApp() {
  return nitroApp$1;
}
runNitroPlugins(nitroApp$1);

function defineRenderHandler(render) {
  const runtimeConfig = useRuntimeConfig();
  return eventHandler(async (event) => {
    const nitroApp = useNitroApp();
    const ctx = { event, render, response: void 0 };
    await nitroApp.hooks.callHook("render:before", ctx);
    if (!ctx.response) {
      if (event.path === `${runtimeConfig.app.baseURL}favicon.ico`) {
        setResponseHeader(event, "Content-Type", "image/x-icon");
        return send(
          event,
          "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7"
        );
      }
      ctx.response = await ctx.render(event);
      if (!ctx.response) {
        const _currentStatus = getResponseStatus(event);
        setResponseStatus(event, _currentStatus === 200 ? 500 : _currentStatus);
        return send(
          event,
          "No response returned from render handler: " + event.path
        );
      }
    }
    await nitroApp.hooks.callHook("render:response", ctx.response, ctx);
    if (ctx.response.headers) {
      setResponseHeaders(event, ctx.response.headers);
    }
    if (ctx.response.statusCode || ctx.response.statusMessage) {
      setResponseStatus(
        event,
        ctx.response.statusCode,
        ctx.response.statusMessage
      );
    }
    return ctx.response.body;
  });
}

const debug = (...args) => {
};
function GracefulShutdown(server, opts) {
  opts = opts || {};
  const options = Object.assign(
    {
      signals: "SIGINT SIGTERM",
      timeout: 3e4,
      development: false,
      forceExit: true,
      onShutdown: (signal) => Promise.resolve(signal),
      preShutdown: (signal) => Promise.resolve(signal)
    },
    opts
  );
  let isShuttingDown = false;
  const connections = {};
  let connectionCounter = 0;
  const secureConnections = {};
  let secureConnectionCounter = 0;
  let failed = false;
  let finalRun = false;
  function onceFactory() {
    let called = false;
    return (emitter, events, callback) => {
      function call() {
        if (!called) {
          called = true;
          return Reflect.apply(callback, this, arguments);
        }
      }
      for (const e of events) {
        emitter.on(e, call);
      }
    };
  }
  const signals = options.signals.split(" ").map((s) => s.trim()).filter((s) => s.length > 0);
  const once = onceFactory();
  once(process, signals, (signal) => {
    debug("received shut down signal", signal);
    shutdown(signal).then(() => {
      if (options.forceExit) {
        process.exit(failed ? 1 : 0);
      }
    }).catch((error) => {
      debug("server shut down error occurred", error);
      process.exit(1);
    });
  });
  function isFunction(functionToCheck) {
    const getType = Object.prototype.toString.call(functionToCheck);
    return /^\[object\s([A-Za-z]+)?Function]$/.test(getType);
  }
  function destroy(socket, force = false) {
    if (socket._isIdle && isShuttingDown || force) {
      socket.destroy();
      if (socket.server instanceof http.Server) {
        delete connections[socket._connectionId];
      } else {
        delete secureConnections[socket._connectionId];
      }
    }
  }
  function destroyAllConnections(force = false) {
    debug("Destroy Connections : " + (force ? "forced close" : "close"));
    let counter = 0;
    let secureCounter = 0;
    for (const key of Object.keys(connections)) {
      const socket = connections[key];
      const serverResponse = socket._httpMessage;
      if (serverResponse && !force) {
        if (!serverResponse.headersSent) {
          serverResponse.setHeader("connection", "close");
        }
      } else {
        counter++;
        destroy(socket);
      }
    }
    debug("Connections destroyed : " + counter);
    debug("Connection Counter    : " + connectionCounter);
    for (const key of Object.keys(secureConnections)) {
      const socket = secureConnections[key];
      const serverResponse = socket._httpMessage;
      if (serverResponse && !force) {
        if (!serverResponse.headersSent) {
          serverResponse.setHeader("connection", "close");
        }
      } else {
        secureCounter++;
        destroy(socket);
      }
    }
    debug("Secure Connections destroyed : " + secureCounter);
    debug("Secure Connection Counter    : " + secureConnectionCounter);
  }
  server.on("request", (req, res) => {
    req.socket._isIdle = false;
    if (isShuttingDown && !res.headersSent) {
      res.setHeader("connection", "close");
    }
    res.on("finish", () => {
      req.socket._isIdle = true;
      destroy(req.socket);
    });
  });
  server.on("connection", (socket) => {
    if (isShuttingDown) {
      socket.destroy();
    } else {
      const id = connectionCounter++;
      socket._isIdle = true;
      socket._connectionId = id;
      connections[id] = socket;
      socket.once("close", () => {
        delete connections[socket._connectionId];
      });
    }
  });
  server.on("secureConnection", (socket) => {
    if (isShuttingDown) {
      socket.destroy();
    } else {
      const id = secureConnectionCounter++;
      socket._isIdle = true;
      socket._connectionId = id;
      secureConnections[id] = socket;
      socket.once("close", () => {
        delete secureConnections[socket._connectionId];
      });
    }
  });
  process.on("close", () => {
    debug("closed");
  });
  function shutdown(sig) {
    function cleanupHttp() {
      destroyAllConnections();
      debug("Close http server");
      return new Promise((resolve, reject) => {
        server.close((err) => {
          if (err) {
            return reject(err);
          }
          return resolve(true);
        });
      });
    }
    debug("shutdown signal - " + sig);
    if (options.development) {
      debug("DEV-Mode - immediate forceful shutdown");
      return process.exit(0);
    }
    function finalHandler() {
      if (!finalRun) {
        finalRun = true;
        if (options.finally && isFunction(options.finally)) {
          debug("executing finally()");
          options.finally();
        }
      }
      return Promise.resolve();
    }
    function waitForReadyToShutDown(totalNumInterval) {
      debug(`waitForReadyToShutDown... ${totalNumInterval}`);
      if (totalNumInterval === 0) {
        debug(
          `Could not close connections in time (${options.timeout}ms), will forcefully shut down`
        );
        return Promise.resolve(true);
      }
      const allConnectionsClosed = Object.keys(connections).length === 0 && Object.keys(secureConnections).length === 0;
      if (allConnectionsClosed) {
        debug("All connections closed. Continue to shutting down");
        return Promise.resolve(false);
      }
      debug("Schedule the next waitForReadyToShutdown");
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve(waitForReadyToShutDown(totalNumInterval - 1));
        }, 250);
      });
    }
    if (isShuttingDown) {
      return Promise.resolve();
    }
    debug("shutting down");
    return options.preShutdown(sig).then(() => {
      isShuttingDown = true;
      cleanupHttp();
    }).then(() => {
      const pollIterations = options.timeout ? Math.round(options.timeout / 250) : 0;
      return waitForReadyToShutDown(pollIterations);
    }).then((force) => {
      debug("Do onShutdown now");
      if (force) {
        destroyAllConnections(force);
      }
      return options.onShutdown(sig);
    }).then(finalHandler).catch((error) => {
      const errString = typeof error === "string" ? error : JSON.stringify(error);
      debug(errString);
      failed = true;
      throw errString;
    });
  }
  function shutdownManual() {
    return shutdown("manual");
  }
  return shutdownManual;
}

function getGracefulShutdownConfig() {
  return {
    disabled: !!process.env.NITRO_SHUTDOWN_DISABLED,
    signals: (process.env.NITRO_SHUTDOWN_SIGNALS || "SIGTERM SIGINT").split(" ").map((s) => s.trim()),
    timeout: Number.parseInt(process.env.NITRO_SHUTDOWN_TIMEOUT || "", 10) || 3e4,
    forceExit: !process.env.NITRO_SHUTDOWN_NO_FORCE_EXIT
  };
}
function setupGracefulShutdown(listener, nitroApp) {
  const shutdownConfig = getGracefulShutdownConfig();
  if (shutdownConfig.disabled) {
    return;
  }
  GracefulShutdown(listener, {
    signals: shutdownConfig.signals.join(" "),
    timeout: shutdownConfig.timeout,
    forceExit: shutdownConfig.forceExit,
    onShutdown: async () => {
      await new Promise((resolve) => {
        const timeout = setTimeout(() => {
          console.warn("Graceful shutdown timeout, force exiting...");
          resolve();
        }, shutdownConfig.timeout);
        nitroApp.hooks.callHook("close").catch((error) => {
          console.error(error);
        }).finally(() => {
          clearTimeout(timeout);
          resolve();
        });
      });
    }
  });
}

const cert = process.env.NITRO_SSL_CERT;
const key = process.env.NITRO_SSL_KEY;
const nitroApp = useNitroApp();
const server = cert && key ? new Server({ key, cert }, toNodeListener(nitroApp.h3App)) : new Server$1(toNodeListener(nitroApp.h3App));
const port = destr(process.env.NITRO_PORT || process.env.PORT) || 3e3;
const host = process.env.NITRO_HOST || process.env.HOST;
const path = process.env.NITRO_UNIX_SOCKET;
const listener = server.listen(path ? { path } : { port, host }, (err) => {
  if (err) {
    console.error(err);
    process.exit(1);
  }
  const protocol = cert && key ? "https" : "http";
  const addressInfo = listener.address();
  if (typeof addressInfo === "string") {
    console.log(`Listening on unix socket ${addressInfo}`);
    return;
  }
  const baseURL = (useRuntimeConfig().app.baseURL || "").replace(/\/$/, "");
  const url = `${protocol}://${addressInfo.family === "IPv6" ? `[${addressInfo.address}]` : addressInfo.address}:${addressInfo.port}${baseURL}`;
  console.log(`Listening on ${url}`);
});
trapUnhandledNodeErrors();
setupGracefulShutdown(listener, nitroApp);
const nodeServer = {};

export { joinRelativeURL as a, getResponseStatus as b, defineRenderHandler as c, defineEventHandler as d, getQuery as e, createError$1 as f, getResponseStatusText as g, getRouteRules as h, useNitroApp as i, joinURL as j, nodeServer as n, proxyRequest as p, sendRedirect as s, useRuntimeConfig as u };
//# sourceMappingURL=nitro.mjs.map
