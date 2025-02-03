# **GCP Workfront Connector**


## **Overview**

This repository contains a **Google Cloud Function** that integrates **Adobe Workfront** with **Google Cloud Storage (GCS)**. It listens for webhook events from Workfront, processes the incoming JSON data, and stores it in a GCS bucket for further analysis or downstream processing.


## **Features**



* Receives Workfront webhook events via HTTP.
* Processes both **single-event** and **batch event** requests.
* Uploads structured JSON data to a designated **Google Cloud Storage (GCS) bucket**.
* Implements **error handling** and **logging** for monitoring.


---


## **Architecture**



1. **Adobe Workfront Webhook** triggers an HTTP request to the **GCP Cloud Function**.
2. The function parses the incoming JSON data.
3. The data is structured and uploaded to **Google Cloud Storage (GCS)** in JSON format.
4. Logs are recorded for debugging and monitoring purposes.


---


## **Project Structure**




```
📂 gcp-connector-workfront/
│── 📜 main.py               # Main Cloud Function script
│── 📜 requirements.txt      # Python dependencies
│── 📜 check_files.sh        # Shell script (possibly for setup/validation)
│── 📜 README.md             # Documentation (this file)


---
```



## **Setup & Deployment**


### **1. Prerequisites**

Ensure you have:



* **Google Cloud SDK** installed (`gcloud` CLI).
* A **Google Cloud Storage (GCS) bucket** created.
* Workfront **webhook configured** to send events to the Cloud Function.


### **2. Install Dependencies**

Run the following command to install required dependencies:




```
pip install -r requirements.txt
```



### **3. Deploy the Cloud Function**

Use the following command to deploy the function:



```
gcloud functions deploy workfront_webhook \
  --runtime python310 \
  --trigger-http \
  --allow-unauthenticated \
  --entry-point workfront_webhook \
  --set-env-vars WORKFRONT_BUCKET_NAME=workfront-bucket-poc
```


Replace `workfront-bucket-poc` with the new **GCS bucket name** where events should be stored if you need to update **GCS Bucket**.


### **4. Configure Workfront Webhook**



* In **Adobe Workfront**, navigate to **Webhooks** settings.

Set the webhook URL as: \

`https://us-central1-candt-voltron.cloudfunctions.net/workfront_webhook`



* 
* Choose the necessary events and enable the webhook.


---


## **How It Works**



* **Step 1:** Workfront sends an event (or batch of events) via HTTP to the Cloud Function.
* **Step 2:** The Cloud Function extracts and validates the JSON data.
* **Step 3:** The function uploads the data to the specified **Google Cloud Storage bucket**.
* **Step 4:** Logging helps monitor the webhook activity.


---


## **Environment Variables**

This function relies on the following environment variables:


<table>
  <tr>
   <td><strong>Variable Name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><code>WORKFRONT_BUCKET_NAME</code>
   </td>
   <td>The GCS bucket where webhook data is stored.
   </td>
  </tr>
</table>



---


## **Error Handling & Logging**



* **Logs:** All logs are available in **Google Cloud Logging**.
* **Retries:** If the upload to GCS fails, an error is logged, and the function raises an exception.


---


## **Future Enhancements**



* Add **Pub/Sub integration** for downstream event processing.
* Implement **authentication & security** for webhook requests.
* Enable **structured logging & monitoring** with Stackdriver.


---


## **Contributing**



1. Fork this repository.
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m "Added new feature"`
4. Push to the branch: `git push origin feature-name`
5. Open a **Pull Request**.
