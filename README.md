# GWA Package

## Installation

Download and install the package on your machine:
```
cd <<working directory>>
git clone https://github.com/kamdickens/wfa.git
pip install -e ./wfa
```

Import the package into your Python script:
```
import gwa_package as gwa
```

## Usage

### `gwa.ona`

- `gwa.ona.clean_email_data(dir, files='all', include_subject=False, engine='c', encoding='latin', delete_old_file=False)`
- `def generate_node_edge_lists(email_data, demographic_data, demographic_key, output_dir, include_subject=False)`
