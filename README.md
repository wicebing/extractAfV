# extractAfV
extract Audio from Video


# to make a environment.yml
conda env export > environment.yml

# TO SET UP ENV
conda env create -f environment.yml

# RUN THE CODE
pull what Video you want to convert into the file "workVideo", the output will be the file "propAudio"

python v2a.py

or you can set the working File as

python v2a.py ["filePath in your setting"] 
    such as => python v2a.py 'C:\\Users\\USER\\Downloads\\setVideo'