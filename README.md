HSN Predictor

For a particular query or product description, finds the 20 most relevant HSN codes

# hsn-predictor

Instructions for Installations

Make sure python is properly installed

Make sure pip is properly installed , [Installing pip if not present](https://pip.pypa.io/en/stable/installation/)

Install virtualenv
virtualenv is a tool to create isolated Python projects. Think of it, as a cleanroom, isolated from other versions of Python and libriries.

Enter this command into terminal

```
sudo pip install virtualenv
```

or if you get an error

```
sudo -H pip install virtualenv
```

1. Run the follwoing command to create the virtual environment

```
python3 -m venv venv
```

2. Activate the virtual environment:

```
source venv/bin/activate
```

3. Intsall required libraries

```
pip install -r requirements.txt
```
