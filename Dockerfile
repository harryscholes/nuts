FROM continuumio/miniconda3:latest
WORKDIR /home
COPY conda_environment.yml install.sh setup.py nuts/
COPY nuts nuts/nuts/
RUN (cd nuts && bash install.sh)
# RUN cd ..
COPY docker/run_me.ipynb ./
EXPOSE 8888
CMD ["/opt/conda/envs/nuts/bin/jupyter", "notebook", "--ip", "0.0.0.0", "--no-browser", "--allow-root"]
