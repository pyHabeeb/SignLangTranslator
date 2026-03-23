# SignLangTranslator

A real-time American Sign Language (ASL) gesture recognition and translation system using DETR (Detection Transformer) and PyTorch.

## 🎯 Project Overview

This project implements an end-to-end pipeline for **real-time ASL gesture detection and translation**. It addresses the communication barrier faced by deaf and hard-of-hearing individuals by automatically recognizing ASL gestures from a live webcam feed and translating them to text labels.

**Key Features:**
- ✅ Fully automated image collection from webcam
- ✅ Bounding box annotation using Label Studio
- ✅ DETR-based deep learning model training
- ✅ Real-time inference with confidence-filtered detection
- ✅ Support for multiple ASL gesture classes
- ✅ End-to-end trainable pipeline with no hand-crafted preprocessing

## 📋 System Architecture

The project follows a linear 5-stage pipeline:
```
Webcam Input
    ↓
Image Collection → Label Studio Annotation → DETR Training → Model Evaluation → Real-Time Inference
```
