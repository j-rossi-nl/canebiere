# Graph Report - canebiere  (2026-10-28)

## Corpus Check
- Large corpus: 43 files · ~1,437,620 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 128 nodes · 211 edges · 18 communities (5 shown, 13 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.87)
- Token cost: 39,957 input · 0 output

## Community Hubs (Navigation)
- Season Notebooks
- Text & Opponent Analysis
- Flask Dashboard Charts
- Dashboard Templates
- Academies Data Prep
- Scrapy Spider
- Scraper Export Pipeline
- Flask Config
- Graphify Workflow Docs
- Website Build Script
- Scraper Project

## God Nodes (most connected - your core abstractions)
1. `notes()` - 12 edges
2. `resultats()` - 9 edges
3. `_resultats()` - 8 edges
4. `build_recent()` - 7 edges
5. `parse(url, div)` - 7 edges
6. `WriteItemPipeline` - 6 edges
7. `CanebiereSpider` - 6 edges
8. `layout.html (AdminLTE base template)` - 6 edges
9. `recent.html (recent news dashboard page)` - 5 edges
10. `plot_recent_match_notes()` - 4 edges

## Surprising Connections (you probably didn't know these)
- `Sidebar link Actualites (build_recent)` --references--> `recent.html (recent news dashboard page)`  [INFERRED]
  dashboard/web/templates/layout.html → dashboard/web/templates/recent.html
- `CanebiereSpider` --uses--> `CanebiereItem`  [INFERRED]
  scraper/canebiere/spiders/canebiere_spider.py → scraper/canebiere/items.py
- `recent.html (recent news dashboard page)` --implements--> `Jinja block script`  [EXTRACTED]
  dashboard/web/templates/recent.html → dashboard/web/templates/layout.html
- `recent.html (recent news dashboard page)` --implements--> `Jinja block my_content`  [EXTRACTED]
  dashboard/web/templates/recent.html → dashboard/web/templates/layout.html
- `parse(url, div)` --references--> `Vega / Vega-Lite / vega-embed CDN libraries`  [EXTRACTED]
  dashboard/web/templates/recent.html → dashboard/web/templates/layout.html

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Recent page Vega-Lite chart specs rendered via parse()** — dashboard_web_templates_recent_plot_recent_match_notes, dashboard_web_templates_recent_plot_recent_player_notes, dashboard_web_templates_recent_plot_recent_player_matchs, dashboard_web_templates_recent_plot_all_player_notes, dashboard_web_templates_recent_plot_all_player_means, dashboard_web_templates_recent_parse [EXTRACTED 1.00]

## Communities (18 total, 13 thin omitted)

### Community 0 - "Season Notebooks"
Cohesion: 0.13
Nodes (8): date_to_season(), date_to_season(), date_to_season(), notes(), resultats(), _resultats(), extract_buts(), unpickle_blaah()

### Community 1 - "Text & Opponent Analysis"
Cohesion: 0.14
Nodes (4): main(), date_to_season(), date_to_season(), lemmatize()

### Community 2 - "Flask Dashboard Charts"
Cohesion: 0.36
Nodes (6): build_recent(), plot_all_player_notes(), plot_all_players_means(), plot_recent_match_notes(), plot_recent_player_matchs(), plot_recent_player_notes()

### Community 3 - "Dashboard Templates"
Cohesion: 0.21
Nodes (13): layout.html (AdminLTE base template), AdminLTE theme, Jinja block my_content, Jinja block script, Sidebar link Actualites (build_recent), Vega / Vega-Lite / vega-embed CDN libraries, recent.html (recent news dashboard page), parse(url, div) (+5 more)

### Community 4 - "Academies Data Prep"
Cohesion: 0.24
Nodes (7): get_by_country(), get_by_country_merged(), load_chartjs_map_data(), load_data(), merge_data(), preprocessed_data(), date_to_season()

## Knowledge Gaps
- **8 isolated node(s):** `canebiere`, `GRAPH_REPORT.md`, `AdminLTE theme`, `context.plot_recent_match_notes (5 derniers matchs)`, `context.plot_recent_player_notes (Les Notes)` (+3 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 55 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `notes()` connect `Season Notebooks` to `Text & Opponent Analysis`, `Academies Data Prep`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **What connects `canebiere`, `GRAPH_REPORT.md`, `AdminLTE theme` to the rest of the system?**
  _8 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Season Notebooks` be split into smaller, more focused modules?**
  _Cohesion score 0.13 - nodes in this community are weakly interconnected._
- **Should `Text & Opponent Analysis` be split into smaller, more focused modules?**
  _Cohesion score 0.14130434782608695 - nodes in this community are weakly interconnected._