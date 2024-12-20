bash<br>
├── data<br>
│   ├── ~$ ideas.docx<br>
│   ├── BeerAdvocate<br>
│   │   ├── beers_BA_clean.csv<br>
│   │   ├── beers.csv<br>
│   │   ├── breweries_BA_clean.csv<br>
│   │   ├── breweries.csv<br>
│   │   ├── content.md<br>
│   │   ├── country_avg_scores_BA.json<br>
│   │   ├── country_year_scores_BA.json<br>
│   │   ├── ratings_BA_clean.csv<br>
│   │   ├── ratings_BA.csv<br>
│   │   ├── reviews_tagged.csv<br>
│   │   ├── reviews.txt.gz<br>
│   │   ├── reviews_with_exp_scores.csv<br>
│   │   ├── reviews_with_exp_stems.pkl<br>
│   │   ├── rev_w_scores.pkl<br>
│   │   ├── users_BA_clean.csv<br>
│   │   └── users.csv<br>
│   ├── expert_terms.json<br>
│   ├── matched_beer_data<br>
│   │   ├── beers.csv<br>
│   │   ├── breweries.csv<br>
│   │   ├── ratings.csv<br>
│   │   ├── users_approx.csv<br>
│   │   └── users.csv<br>
│   ├── RateBeer<br>
│   │   ├── beers.csv<br>
│   │   ├── beers_RB_clean.csv<br>
│   │   ├── breweries.csv<br>
│   │   ├── breweries_RB_clean.csv<br>
│   │   ├── content.md<br>
│   │   ├── ratings_RB_clean.csv<br>
│   │   ├── ratings_RB.csv<br>
│   │   ├── reviews_tagged.csv<br>
│   │   ├── reviews.txt.gz<br>
│   │   ├── reviews_with_exp_stems.pkl<br>
│   │   ├── rev_w_scores.pkl<br>
│   │   ├── users.csv<br>
│   │   └── users_RB_clean.csv<br>
│   └── word_occurences<br>
│       ├── appearance.json<br>
│       ├── brewing.json<br>
│       ├── flavor.json<br>
│       ├── mouthfeel.json<br>
│       ├── off_flavors.json<br>
│       └── technical.json<br>
├── docs<br>
│   ├── 404.html<br>
│   ├── about.markdown<br>
│   ├── assets<br>
│   │   └── css<br>
│   │       ├── beautifuljekyll.css<br>
│   │       └── custom.css<br>
│   ├── _config.yml<br>
│   ├── favicon.ico<br>
│   ├── Gemfile<br>
│   ├── Gemfile.lock<br>
│   ├── index.markdown<br>
│   ├── pics<br>
│   │   ├── appearance_score_stylewise.png<br>
│   │   ├── avatar.webp<br>
│   │   ├── BA_exp_nonexp_eng_nongl_evol.png<br>
│   │   ├── blacktan.jpg<br>
│   │   ├── brewing_score_stylewise.png<br>
│   │   ├── corr_matrix_all_BA.png<br>
│   │   ├── corr_matrix_all_RB.png<br>
│   │   ├── country_expertness_evol_BA.png<br>
│   │   ├── expertness_country_BA.png<br>
│   │   ├── expertness_score_stylewise.png<br>
│   │   ├── exp_nonexp_evol.png<br>
│   │   ├── flavour_score_stylewise.png<br>
│   │   ├── gueuze.png<br>
│   │   ├── improve_aggr_ba.png<br>
│   │   ├── improve_aggr_rb.png<br>
│   │   ├── mouthfeel_score_stylewise.png<br>
│   │   ├── navbar.jpg<br>
│   │   ├── off_flavours_score_stylewise.png<br>
│   │   ├── post.jpg<br>
│   │   ├── RB_exp_nonexp_eng_nongl_evol.png<br>
│   │   ├── technical_score_stylewise.png<br>
│   │   ├── wheel.jpg<br>
│   │   └── word_cloud_BA_RB.png<br>
│   ├── plots<br>
│   │   ├── big_events.html<br>
│   │   ├── demo.html<br>
│   │   ├── evolution_countries_BA.html<br>
│   │   ├── evolution_countries_RB.html<br>
│   │   ├── graphic-stroke-animation.html<br>
│   │   ├── mean_countries_BA.html<br>
│   │   ├── mean_countries_RB.html<br>
│   │   ├── metric_categories_plot.html<br>
│   │   ├── pie_categories.html<br>
│   │   ├── radar_importance.html<br>
│   │   ├── test_plot.html<br>
│   │   └── text_highlight.html<br>
│   ├── _posts<br>
│   │   └── 2024-12-05-welcome-to-jekyll.markdown<br>
│   └── test.py<br>
├── README.md<br>
├── results.ipynb<br>
├── src<br>
│   ├── graphs<br>
│   │   ├── big_events<br>
│   │   │   └── big_events.html<br>
│   │   ├── categories_importance<br>
│   │   │   └── radar_importance.html<br>
│   │   ├── Evolution_countries<br>
│   │   │   ├── country_avg_scores_BA.json<br>
│   │   │   ├── country_avg_scores_RB.json<br>
│   │   │   ├── country_year_scores_BA.json<br>
│   │   │   ├── country_year_scores_RB.json<br>
│   │   │   ├── evolution_countries_BA.html<br>
│   │   │   ├── evolution_countries_RB.html<br>
│   │   │   ├── mean_countries_BA.html<br>
│   │   │   └── mean_countries_RB.html<br>
│   │   ├── metric&sliders<br>
│   │   │   ├── Categorical_avg_evolution.json<br>
│   │   │   ├── data_and_plot.ipynb<br>
│   │   │   └── metric_categories_plot.html<br>
│   │   ├── pie_categories<br>
│   │   │   └── pie_categories.html<br>
│   │   ├── text_highlight<br>
│   │   │   ├── expanded_metric.ipynb<br>
│   │   │   ├── expanded_metric.json<br>
│   │   │   ├── reviews.js<br>
│   │   │   └── text_highlight.html<br>
│   │   └── title_animation<br>
│   │       └── graphic-stroke-animation.html<br>
│   └── scripts<br>
│       ├── country_analysis<br>
│       │   ├── ADA_Beers (2).ipynb<br>
│       │   ├── ba_countries_analysis.ipynb<br>
│       │   ├── c_an_utilis.py<br>
│       │   ├── country_avg_scores_RB.json<br>
│       │   ├── country_year_scores_RB.json<br>
│       │   └── rb_countries_analysis.ipynb<br>
│       ├── data_cleaning<br>
│       │   ├── data_cleaning.ipynb<br>
│       │   ├── data_cleaning.py<br>
│       │   ├── load_file.py<br>
│       │   └── __pycache__<br>
│       │       ├── data_cleaning.cpython-311.pyc<br>
│       │       └── load_file.cpython-311.pyc<br>
│       ├── EDA<br>
│       │   └── ADA_Beers.ipynb<br>
│       ├── embedding<br>
│       │   ├── Embedding_output.png<br>
│       │   └── embedding_work.ipynb<br>
│       ├── expert_analysis<br>
│       │   ├── analysis_helper.py<br>
│       │   ├── ba_analysis_exp_metric.ipynb<br>
│       │   ├── expert_analysis.py<br>
│       │   ├── __pycache__<br>
│       │   │   └── expert_analysis.cpython-311.pyc<br>
│       │   └── rb_analysis_exp_metric.ipynb<br>
│       ├── expert_metric<br>
│       │   ├── add_exp.ipynb<br>
│       │   ├── add_exp.py<br>
│       │   ├── Expert_metric.ipynb<br>
│       │   ├── expert_metric.py<br>
│       │   ├── exp_stem_extractor.ipynb<br>
│       │   ├── exp_stem_extractor.py<br>
│       │   └── __pycache__<br>
│       │       └── expert_metric.cpython-311.pyc<br>
│       ├── helpers.py<br>
│       ├── lang_tagger<br>
│       │   ├── lang_tagger_Ale.ipynb<br>
│       │   ├── lang_tagger.py<br>
│       │   └── __pycache__<br>
│       ├── load_file.py<br>
│       ├── __pycache__<br>
│       │   ├── helpers.cpython-311.pyc<br>
│       │   ├── load_file.cpython-311.pyc<br>
│       │   └── load_file.cpython-312.pyc<br>
│       ├── quality_over_year<br>
│       │   └── quality_over_year.ipynb<br>
│       ├── review_comparison<br>
│       │   └── review_comparison.ipynb<br>
│       └── word_occurences<br>
│           ├── pair_occurences.ipynb<br>
│           ├── word_cloud.py<br>
│           └── world_cloud.ipynb<br>
└── structure.md<br>
