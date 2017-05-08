#include "ros/ros.h"
#include "opencv2/opencv.hpp"
#include "std_msgs/String.h"
#include <sensor_msgs/Image.h>
#include <sensor_msgs/image_encodings.h>
#include <cv_bridge/cv_bridge.h>

using namespace std;
using namespace cv;

/*
*   Convert openCV image into ROS image message
*/
sensor_msgs::Image imageToMsg(Mat &img)
{
    cv_bridge::CvImage img_bridge;
    sensor_msgs::Image img_msg;     // Message to be sent
    std_msgs::Header header; // empty header

    header.seq = 1; // user defined counter
    header.stamp = ros::Time::now(); // time

    img_bridge = cv_bridge::CvImage(header, sensor_msgs::image_encodings::RGB8, img);
    img_bridge.toImageMsg(img_msg); // from cv_bridge to sensor_msgs::Image

    return img_msg;
}



int main(int argc, char **argv)
{
    ros::init(argc, argv, "image_grabber"); // Init ROS
    ros::NodeHandle nh; // Node handler
    ros::Publisher pub = nh.advertise<sensor_msgs::Image>("camera_image", 5);   // Image publisher

    Mat cameraFrame;
    VideoCapture camera(0); // Open default camera 0

    if (!camera.isOpened())
    {
        cout << "ERROR: Cannot open camera!" << endl;
        return 0;
    }

    while(1)
    {
        camera.read(cameraFrame);   // Grab image from webcam

        sensor_msgs::Image img_msg = imageToMsg(cameraFrame);   // Convert webcam image to a ROS message
        pub.publish(img_msg); // Publish image on ROS
        ros::spinOnce();
    }

    return 0;
}
