# TensorTest
This project uses TensorFlow to predict web API status codes based on API input.

## Running the application
1. Install and activate pip
    ```sudo easy_install pip
    pip install --upgrade virtualenv
    virtualenv --system-site-packages
    source ./bin/activate
    ```

1. Install tensorflow:
    ```
    pip install --upgrade tensorflow
    ```
1. Install the requirements for the web service:
    ```
    pip install -r requirements.txt
    ```
1. Run the flask web server:
    ```
    python src/service/resources.py
    ```
