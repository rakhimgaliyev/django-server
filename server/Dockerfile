FROM continuumio/miniconda3
RUN mkdir /backend_diploma
WORKDIR /backend_diploma
COPY requirements.txt /backend_diploma/
RUN conda config --append channels conda-forge
RUN conda config --add channels conda-forge
RUN conda config --set channel_priority strict
RUN conda install --file requirements.txt
RUN pip install python-tsp
RUN pip install scikit-learn
RUN pip install numpy
COPY . /backend_diploma/