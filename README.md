# ITU WTSA24 Hackathon - AI Bharat 5G/6G Sandbox 

This is our submission to this hackathon from Indian Institute of Information Technology, Allahabad.

Our project "Eyes from above" aims to aid cleaning of rivers by detecting and reporting waste accumulation on river bed.

Our project consists of several components which work together performing their individual duties. Components and their roles are:

1. Non-RT RIC:

    Role: Non-RT RIC provides long-term network management and training for AI/ML models that will be used in the xApp. In your case, it will:
        Train the river detection and waste detection models using historical data (satellite images and previous flight data).
        Optimize the models periodically and update them on Near-RT RIC when improvements are made.
    Tasks:
        Maintain training datasets (satellite images, waste site identification).
        Develop policies for drone operation and update them periodically based on performance data.

2. Near-RT RIC:

    Role: Near-RT RIC hosts the xApp, interacts with the RAN components in real-time, and makes immediate decisions based on the data provided by the drone and the network.

    Components:
        xApp: This is the core application that handles both drone navigation and waste detection.
        ML Models: Integrated in the xApp, including:
            River Detection Model: This is the pre-built model that processes satellite images and identifies river edges.
            Waste Detection Model: An object detection model that analyzes images captured by the drone and identifies waste disposal sites.

    Tasks:
        Receive and process satellite images to identify the river paths using the River Detection Model.
        Coordinate drone movement along the river path using 5G connectivity, ensuring it stays close to the river's edge.
        Collect real-time data from the drone (e.g., camera feeds, GPS locations) and analyze the feed to detect waste using the Waste Detection Model.
        Log locations where waste is detected and relay the information to external systems or for further analysis.

3. UAV:

    Role: The drone is the physical entity that follows the path provided by the xApp and collects real-time data. The drone communicates with the RAN (through gNB/eNB) using 5G/4G for reliable and high-speed data transfer.

    Tasks:
        Follow the river edge path by receiving commands from the xApp hosted on Near-RT RIC.
        Capture high-resolution images as it flies along the river.
        Send the images back to the xApp for real-time processing.
        Upon detecting waste, log the location and capture additional data (images/videos) as needed.

4. RAN Nodes (gNB/eNB):

    Role: These are the base stations responsible for providing 5G/4G connectivity to the drone in the field. They ensure continuous communication between the drone and the xApp running on the Near-RT RIC.

    Tasks:
        Provide low-latency connectivity to the drone for command/control signals.
        Enable high-bandwidth data transmission for real-time image/video streams.
        Support mobility management as the drone moves along the river.

5. Satellite Image Processing:

    River Path Detection: The satellite images are processed by the ML engine integrated into the xApp. This model analyzes the image to identify the river path.
    Coordinate Generation: Based on the image analysis, the river path is converted into a series of GPS coordinates that the drone will follow.

6. Waste Detection:

    As the drone follows the path, the xApp continuously analyzes the drone’s camera feed using the Waste Detection Model. When waste is detected:
        The xApp logs the location (using the drone’s GPS) and saves relevant images.
        This data can be sent back to the Non-RT RIC for further analysis or reporting.
