# Azure Recommender System

This is a simple content-based recommender system for films created for the DEPI project. The application is built using Streamlit and deployed on Azure App Service.

## Features

- Load and display a list of film titles.
- Provide film recommendations based on a selected film.
- Display a logo in the top left corner of the application.

## Installation

1. **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/azure-recommender-system.git
    cd azure-recommender-system
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Run the application:**

    ```sh
    streamlit run App/app.py
    ```

## Deployment on Azure

### Step 1: Prepare Your Application

1. **Ensure your application is working locally.**
2. **Create a `requirements.txt` file** to list all the dependencies. You can generate this file using the following command:

    ```sh
    pip freeze > requirements.txt
    ```

3. **Create a `Procfile`** to specify the command to run your Streamlit app. The `Procfile` should contain the following line:

    ```
    web: streamlit run [app.py](http://_vscodecontentref_/#%7B%22uri%22%3A%7B%22%24mid%22%3A1%2C%22fsPath%22%3A%22d%3A%5C%5CAzureRecommender%5C%5CApp%5C%5Capp.py%22%2C%22_sep%22%3A1%2C%22path%22%3A%22%2FD%3A%2FAzureRecommender%2FApp%2Fapp.py%22%2C%22scheme%22%3A%22file%22%7D%7D) --server.port $PORT
    ```

### Step 2: Create an Azure App Service

1. **Log in to the Azure Portal**: [https://portal.azure.com](https://portal.azure.com)
2. **Create a new Resource Group** (if you don't have one already):
    - Go to "Resource groups" and click "Add".
    - Fill in the required details and click "Review + create".

3. **Create a new App Service**:
    - Go to "App Services" and click "Add".
    - Fill in the required details:
        - **Resource Group**: Select the resource group you created.
        - **Name**: Give your app a unique name.
        - **Publish**: Code.
        - **Runtime stack**: Python 3.x.
        - **Region**: Select a region close to you.
    - Click "Review + create" and then "Create".

### Step 3: Deploy Your Application

1. **Install the Azure CLI**: If you don't have it installed, you can download it from [here](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli).

2. **Log in to Azure**:

    ```sh
    az login
    ```

3. **Change to your project directory**:

    ```sh
    cd path/to/your/project
    ```

4. **Initialize a Git repository** (if you haven't already):

    ```sh
    git init
    git add .
    git commit -m "Initial commit"
    ```

5. **Create a deployment user**:

    ```sh
    az webapp deployment user set --user-name <username> --password <password>
    ```

6. **Configure the deployment**:

    ```sh
    az webapp deployment source config-local-git --name <app-name> --resource-group <resource-group>
    ```

    This command will return a Git URL. Note it down.

7. **Add the Azure remote to your Git repository**:

    ```sh
    git remote add azure <git-url>
    ```

8. **Push your code to Azure**:

    ```sh
    git push azure master
    ```

### Step 4: Configure the App Service

1. **Go to the Azure Portal** and navigate to your App Service.
2. **Go to "Configuration"** under "Settings".
3. **Add a new application setting**:
    - **Name**: `PORT`
    - **Value**: `8000`
4. **Save the configuration**.

### Step 5: Access Your Application

Once the deployment is complete, you can access your Streamlit app using the URL provided by Azure App Service.

## License

This project is licensed under the MIT License. See the LICENSE file for details.