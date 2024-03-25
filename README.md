# MedSearch: Vector-Powered X-Ray Image Similarity Search

## Overview

MedSearch explores the application of vector similarity search techniques to medical image retrieval.  The core focus is on developing a proof-of-concept system that enables users to find visually similar X-ray images within a dataset using an uploaded query image.

## Use Cases

- Radiology (Proof-of-Concept): Provides a tool for radiologists to quickly reference visually similar X-ray images, potentially aiding in diagnosis or identifying subtle patterns.
- Research (Exploration): Allows researchers to investigate potential relationships between X-ray images based on visual similarity.
- Education (Demonstration): Serves as a learning aid for understanding image representations and similarity search in a medical context.
Tech Stack

## Tech Stack

### Backend:
- Python
- Flask (Web framework)
- Milvus (Vector similarity search database)
- TensorFlow (ResNet-50 model)

### Frontend:
- HTML, CSS
- JavaScript (Fetch API or AJAX for API interactions)

### Databases:
- PostGresSQL (Image storage and metadata)

### Dataset
- ChestX-ray14: A publicly available X-ray dataset suitable for initial prototyping.

## System Architecture
### Deep Learning Model:
- ResNet-50 (pre-trained on ImageNet): This model extracts meaningful feature vectors representing the visual content of X-ray images. We leverage a pre-trained model for efficiency and to avoid extensive training for this prototype.

### Vector Similarity Search Database:
- Milvus: Optimized for fast and efficient similarity searches on high-dimensional vector data.


## Workflow
- Image Preprocessing: Incoming X-rays are resized and normalized for consistency.

- Feature Extraction:  The pre-trained ResNet-50 model (without the final classification layer) transforms each X-ray image into a high-dimensional feature vector.

- Vector Storage:  Milvus stores the extracted feature vectors, enabling fast similarity comparisons.

- Query Image:  The user uploads a query X-ray image.

## Search:

* The query image's feature vector is generated.
* Milvus performs a vector similarity search, finding the most visually similar images within the dataset.

#### Results: The backend returns the images and IDs of the most similar X-rays images found.

## Frontend (Minimal for Prototype)

A basic web interface allows users to upload an image and display the X-ray images retrieved along with their IDs.

## Results

MedSearch successfully demonstrates the core principles of vector similarity search for medical image retrieval.  Users can upload a query image and see visually similar X-ray images retrieved from the dataset.

## Future Enhancements

- Model Fine-tuning: Improve similarity results for the X-ray domain by fine-tuning the ResNet-50 model on the X-ray dataset.
- Metadata Search: Integrate metadata (e.g., diagnosis) with vector search for more focused retrieval.
- Scalability: Investigate database optimizations and distributed architectures to accommodate larger datasets.
