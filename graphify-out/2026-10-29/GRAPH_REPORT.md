# Graph Report - canebiere  (2026-10-29)

## Corpus Check
- 34 files · ~318,361 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 59 file(s) not represented in the graph (top: .jsonl 18, .css 14, .map 6)

## Summary
- 598 nodes · 1120 edges · 52 communities (35 shown, 17 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 109 edges (avg confidence: 0.85)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `448abeb6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- season.py
- Ee
- routes.py
- parse(url, div)
- Season
- canebiere_spider.py
- t
- config.py
- Graphify Knowledge Graph (graphify-out/)
- generate_website.sh
- jquery.min.js
- canebiere
- jquery.slim.min.js
- bootstrap.bundle.min.js
- jquery.js
- jquery.slim.js
- bootstrap.bundle.js
- bootstrap.js
- getReferenceOffsets
- Animation
- e
- bootstrap.min.js
- domManip
- l
- matcherFromTokens
- matcherFromTokens
- getBoundingClientRect
- domManip
- flip
- getBoundaries
- getOffsetParent
- find
- destroy
- expectSync
- expectSync
- La Canebière Académie
- resolve
- getWidthOrHeight
- buildParams
- resolve
- inspect
- createCache
- on
- on
- Ie

## God Nodes (most connected - your core abstractions)
1. `getBoundaries()` - 13 edges
2. `Ee()` - 12 edges
3. `getBoundingClientRect()` - 11 edges
4. `$e()` - 11 edges
5. `e()` - 11 edges
6. `Season` - 11 edges
7. `getOffsetRectRelativeToArbitraryNode()` - 10 edges
8. `Pe()` - 10 edges
9. `Ze()` - 10 edges
10. `e()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `main()` --calls--> `season_page_name()`  [EXTRACTED]
  build_site.py → utils/articles.py
- `main()` --calls--> `season_pages()`  [EXTRACTED]
  build_site.py → utils/articles.py
- `main()` --calls--> `render_season()`  [EXTRACTED]
  build_site.py → utils/season.py
- `o()` --indirect_call--> `e()`  [INFERRED]
  dashboard/web/static/plugins/bootstrap/js/bootstrap.bundle.min.js → dashboard/web/static/plugins/bootstrap/js/bootstrap.min.js
- `Ie()` --indirect_call--> `Pe()`  [INFERRED]
  dashboard/web/static/plugins/jquery/jquery.min.js → dashboard/web/static/plugins/bootstrap/js/bootstrap.bundle.min.js

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Recent page Vega-Lite chart specs rendered via parse()** — dashboard_web_templates_recent_plot_recent_match_notes, dashboard_web_templates_recent_plot_recent_player_notes, dashboard_web_templates_recent_plot_recent_player_matchs, dashboard_web_templates_recent_plot_all_player_notes, dashboard_web_templates_recent_plot_all_player_means, dashboard_web_templates_recent_parse [EXTRACTED 1.00]

## Communities (52 total, 17 thin omitted)

### Community 0 - "season.py"
Cohesion: 0.06
Nodes (25): main(), render(), get_by_country(), get_by_country_merged(), load_chartjs_map_data(), load_data(), merge_data(), preprocessed_data() (+17 more)

### Community 1 - "Ee"
Cohesion: 0.18
Nodes (18): A(), Oe(), be(), C(), Ee(), F(), ge(), H() (+10 more)

### Community 2 - "routes.py"
Cohesion: 0.36
Nodes (6): build_recent(), plot_all_player_notes(), plot_all_players_means(), plot_recent_match_notes(), plot_recent_player_matchs(), plot_recent_player_notes()

### Community 3 - "parse(url, div)"
Cohesion: 0.21
Nodes (13): layout.html (AdminLTE base template), AdminLTE theme, Jinja block my_content, Jinja block script, Sidebar link Actualites (build_recent), Vega / Vega-Lite / vega-embed CDN libraries, recent.html (recent news dashboard page), parse(url, div) (+5 more)

### Community 6 - "t"
Cohesion: 0.27
Nodes (10): be(), ce(), Ee(), fe(), P(), se(), t(), l() (+2 more)

### Community 11 - "jquery.min.js"
Cohesion: 0.10
Nodes (11): Ae(), ct(), de(), dt(), _e(), et(), ke(), pt() (+3 more)

### Community 18 - "jquery.slim.min.js"
Cohesion: 0.11
Nodes (8): ke(), mt(), nt(), p(), T(), tt(), V(), X()

### Community 19 - "bootstrap.bundle.min.js"
Cohesion: 0.10
Nodes (38): Be(), ct(), dt(), $e(), et(), Fe(), ft(), Ge() (+30 more)

### Community 20 - "jquery.js"
Cohesion: 0.06
Nodes (11): boxModelAdjustment(), computeStyleTests(), createCache(), cache(), curCSS(), dataAttr(), finalPropName(), getData() (+3 more)

### Community 21 - "jquery.slim.js"
Cohesion: 0.06
Nodes (10): camelCase(), computeStyleTests(), dataAttr(), fcamelCase(), finalPropName(), getData(), getDefaultDisplay(), roundPixelMeasures() (+2 more)

### Community 22 - "bootstrap.bundle.js"
Cohesion: 0.07
Nodes (9): allowedAttribute(), _createClass(), _defineProperties(), _defineProperty(), getSpecialTransitionEndEvent(), _objectSpread2(), ownKeys(), sanitizeHtml() (+1 more)

### Community 23 - "bootstrap.js"
Cohesion: 0.10
Nodes (9): allowedAttribute(), _createClass(), _defineProperties(), _defineProperty(), getSpecialTransitionEndEvent(), _objectSpread2(), ownKeys(), sanitizeHtml() (+1 more)

### Community 24 - "getReferenceOffsets"
Cohesion: 0.15
Nodes (14): applyStyle(), applyStyleOnLoad(), computeAutoPlacement(), enableEventListeners(), findIndex(), getArea(), getReferenceNode(), getReferenceOffsets() (+6 more)

### Community 25 - "Animation"
Cohesion: 0.15
Nodes (14): adoptValue(), ajaxConvert(), ajaxHandleResponses(), Animation(), camelCase(), createFxNow(), createTween(), defaultPrefilter() (+6 more)

### Community 26 - "e"
Cohesion: 0.25
Nodes (9): b(), bt(), mt(), B(), ce(), e(), L(), R() (+1 more)

### Community 27 - "bootstrap.min.js"
Cohesion: 0.31
Nodes (10): at(), e(), i(), l(), n(), o(), r(), s() (+2 more)

### Community 28 - "domManip"
Cohesion: 0.18
Nodes (13): buildFragment(), buildParams(), disableScript(), DOMEval(), domManip(), getAll(), isArrayLike(), manipulationTarget() (+5 more)

### Community 29 - "l"
Cohesion: 0.29
Nodes (8): d(), I(), l(), M(), qt(), w(), lt(), st()

### Community 30 - "matcherFromTokens"
Cohesion: 0.20
Nodes (12): addCombinator(), condense(), createPositionalPseudo(), elementMatcher(), markFunction(), matcherFromGroupMatchers(), matcherFromTokens(), multipleContexts() (+4 more)

### Community 31 - "matcherFromTokens"
Cohesion: 0.20
Nodes (12): addCombinator(), condense(), createPositionalPseudo(), elementMatcher(), markFunction(), matcherFromGroupMatchers(), matcherFromTokens(), multipleContexts() (+4 more)

### Community 32 - "getBoundingClientRect"
Cohesion: 0.36
Nodes (10): getBordersSize(), getBoundingClientRect(), getClientRect(), getOffsetRectRelativeToArbitraryNode(), getScroll(), getSize(), getViewportOffsetRectRelativeToArtbitraryNode(), getWindowSizes() (+2 more)

### Community 33 - "domManip"
Cohesion: 0.24
Nodes (10): buildFragment(), disableScript(), DOMEval(), domManip(), getAll(), manipulationTarget(), nodeName(), remove() (+2 more)

### Community 34 - "flip"
Cohesion: 0.29
Nodes (8): arrow(), clockwise(), flip(), getOppositePlacement(), getOppositeVariation(), getOuterSizes(), getPopperOffsets(), inner()

### Community 35 - "getBoundaries"
Cohesion: 0.43
Nodes (8): attachToScrollParents(), getBoundaries(), getFixedPositionOffsetParent(), getParentNode(), getScrollParent(), getStyleComputedProperty(), isFixed(), setupEventListeners()

### Community 36 - "getOffsetParent"
Cohesion: 0.32
Nodes (8): computeStyle(), findCommonOffsetParent(), getOffsetParent(), getRoot(), getRoundedOffsets(), getSupportedPropertyName(), isOffsetContainer(), preventOverflow()

### Community 37 - "find"
Cohesion: 0.38
Nodes (7): find(), hide(), isModifierRequired(), isNumeric(), offset(), parseOffset(), toValue()

### Community 38 - "destroy"
Cohesion: 0.40
Nodes (5): destroy(), disableEventListeners(), getWindow(), isModifierEnabled(), removeEventListeners()

### Community 39 - "expectSync"
Cohesion: 0.50
Nodes (4): expectSync(), leverageNative(), returnTrue(), safeActiveElement()

### Community 40 - "expectSync"
Cohesion: 0.50
Nodes (4): expectSync(), leverageNative(), returnTrue(), safeActiveElement()

### Community 41 - "La Canebière Académie"
Cohesion: 0.50
Nodes (3): En local, La Canebière Académie, Le pipeline

### Community 42 - "resolve"
Cohesion: 0.67
Nodes (3): Identity(), resolve(), Thrower()

### Community 43 - "getWidthOrHeight"
Cohesion: 0.67
Nodes (3): boxModelAdjustment(), curCSS(), getWidthOrHeight()

### Community 44 - "buildParams"
Cohesion: 0.67
Nodes (3): buildParams(), isArrayLike(), toType()

### Community 45 - "resolve"
Cohesion: 0.67
Nodes (3): Identity(), resolve(), Thrower()

### Community 51 - "Ie"
Cohesion: 0.40
Nodes (6): Ie(), le(), Re(), ve(), we(), ye()

## Knowledge Gaps
- **8 isolated node(s):** `canebiere`, `context.plot_all_player_means (Les Moyennes)`, `context.plot_all_player_notes`, `context.plot_recent_match_notes (5 derniers matchs)`, `context.plot_recent_player_matchs (Les Joueurs)` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 193 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `e()` connect `e` to `Ee`, `t`, `jquery.min.js`, `jquery.slim.min.js`, `jquery.js`, `jquery.slim.js`?**
  _High betweenness centrality (0.187) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `Ee()` (e.g. with `t()` and `e()`) actually correct?**
  _`Ee()` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `canebiere`, `context.plot_all_player_means (Les Moyennes)`, `context.plot_all_player_notes` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `season.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05712050078247261 - nodes in this community are weakly interconnected._
- **Why does `Pe()` connect `bootstrap.bundle.min.js` to `Ee`, `Ie`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `$e()` (e.g. with `l()` and `t()`) actually correct?**
  _`$e()` has 3 INFERRED edges - model-reasoned connections that need verification._
- **Should `jquery.min.js` be split into smaller, more focused modules?**
  _Cohesion score 0.09846153846153846 - nodes in this community are weakly interconnected._