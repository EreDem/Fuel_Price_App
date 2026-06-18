# Fuel Smart

🚀 **Live Demo:** https://fuelsmart.expo.app

Fuel Smart is a mobile application prototype for predicting fuel prices based on historical and contextual data. It combines a **neural network built from scratch in NumPy**, a FastAPI backend, and a React Native (Expo) frontend into a single end-to-end system.

The goal was not just to train a model, but to build and validate an actual product end to end.

---

## Tech Stack

| Layer    | Technology                                   |
|----------|----------------------------------------------|
| Model    | Python, NumPy — custom MLP, no ML frameworks |
| Backend  | FastAPI (REST API)                           |
| Frontend | React Native / Expo                          |

---

## Status

**Complete prototype — tested as a product, then discontinued**

- The full system (frontend → backend → model) is implemented and was deployed live
- The end-to-end prediction pipeline works
- The project was tested as a real product and later **discontinued due to insufficient market demand**

It remains a complete, working demonstration of building and debugging an ML system from the ground up.

---

## Highlight: Diagnosing a Mean-Prediction Bug

Early on, the model collapsed to predicting the **mean** of the target values for every input — a common but easy-to-miss failure mode.

I traced this to the combination of **MSE loss and price outliers**: large outliers dominated the squared-error term, so the model minimized loss by collapsing toward the average. Clipping the price outliers restored meaningful, input-dependent predictions.

This kind of debugging — understanding *why* a model misbehaves rather than just swapping architectures — was the most valuable part of the project.

---

## Features

- Mobile UI built with React Native / Expo
- FastAPI backend serving predictions via REST API
- Custom Multi-Layer Perceptron (MLP) implemented from scratch using NumPy
- End-to-end ML pipeline (data → preprocessing → prediction → UI)
- Modular architecture for easy model iteration
- Online deployment (accessible prototype)

---

## Architecture

\`\`\`mermaid
flowchart LR
    A[React Native App] --> B[FastAPI Backend]
    B --> C[Preprocessing]
    C --> D[Custom MLP Model]
    D --> B
    B --> A
\`\`\`

---

## What I Learned

- Implementing a neural network from scratch in NumPy (forward/backward pass, training loop)
- Diagnosing and fixing real training failures (mean-prediction caused by MSE + outliers)
- Serving an ML model through a REST API with FastAPI
- Connecting a model to a real frontend with React Native / Expo
- Validating a product idea against actual market demand
