conda create -n bv03 python=3.12 --yes
call conda activate bv03
conda install python-graphviz --yes
pip install -r requirements.txt

:: Confirm activation
echo Virtual environment "bv03" activated. Ready to install packages.
echo Use `deactivate` to exit the virtual environment.