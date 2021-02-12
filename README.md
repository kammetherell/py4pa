# GWA Package

## Installation

Download and install the package on your machine:
```
cd <<working directory>>
git clone https://github.com/kammetherell/pypas.git
pip install -e ./pypas
```

If you need to bypass SSL verification on your machine (if you are behind a proxy for example), you can use the following install command:
```
git -c http.sslVerify=false clone https://github.com/kamdickens/pypas.git
pip install -e ./pypas --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

Import the package into your Python script:
```
import pypas
```

## Usage

### `pypas.ona`

- `pypas.ona.clean_email_data(dir, files='all', include_subject=False, engine='c', encoding='latin', delete_old_file=False)`
- `pypas.ona.generate_node_edge_lists(email_data, demographic_data, demographic_key, output_dir, include_subject=False)`
- `pypas.ona.generate_nx_digraph(node_list, edge_list)`
- `pypas.ona.calc_density(df_nodes, df_edges, target_attribute)`
- `pypas.ona.calc_modularity(df_nodes, df_edges, target_attribute, weighted=False, direction='outbound')`

### `pypas.arm`

- `pypas.arm.concat_fields(df, fields)`

### `pypas.visualisation`

- `pypas.visualisation.gen_expn_colors()`
- `pypas.visualisation.gen_gradient_cmap(start, end, steps=50)`

### `pypas.nlp`

### `pypas.email_helper`

- `pypas.email_helper.send_plain_text_email(server, sender, recip, subject, body)`

### `pypas.web_scraping`

- `pypas.web_scraping.get_random_useragent(browser=None):`
- `pypas.web_scraping.get_visier_data_connection(data_connector_id, user, pword, api_key, company,fName=None)`

### `pypas.misc`

- `pypas.misc.csv_to_utf8(file)`
- `pypas.misc.upgradeAllPackages()`
- `pypas.misc.installPackage(package)`
- `pypas.misc.getDateTimeStamp(time=True)`
- `pypas.misc.continuous_logging(msg)`
