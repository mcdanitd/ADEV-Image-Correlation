clc
clear all
close all

img = imread('Straw 2.jpg');
hsvImg = rgb2hsv(img);

upperHue = 0.1;
lowerHue = 0.9;
lowerSat = 0.6;
sizeThreshMin = 200;    %will have to adjust as we get closer to the fruit.
sizeThreshMax = 2000;   %will have to adjust as we get closer to the fruit.
% the maximum size threshold given in for this is designed to eliminate
% fruit that are bunched closely together.  We currently do not have a way
% to recognize that an image shows two overlapping strawberries.  The
% solution to this may be in using depth camera information on the objects
% that the maximum size threshold is filtering out.

mask = zeros(size(img,1), size(img,2));
if (upperHue > lowerHue)
    redIndex = find(hsvImg(:,:,1) < upperHue & hsvImg(:,:,1) > lowerHue & hsvImg(:,:,2) > lowerSat);
else
    redIndex = find((hsvImg(:,:,1) < upperHue | hsvImg(:,:,1) > lowerHue) & hsvImg(:,:,2) > lowerSat);
end

mask(redIndex) = 1;

imshow(img)
figure()
imshow(mask)

mask = imdilate(mask, strel('disk',3,4));
figure()
imshow(mask)

mask = imerode(mask, strel('disk',4,4));
figure()
imshow(mask)

%mask = imdilate(mask, strel('square', 6));
mask = imdilate(mask, strel('disk',4,4));
figure()
imshow(mask)

%mask = imerode(mask, strel('square', 9));
mask = imerode(mask, strel('disk',4,4));
figure()
imshow(mask)

[m_label,n] = bwlabel(mask);
max(m_label(:));

for i = 1:n
    f = size(find(m_label == i));
    if (f < sizeThreshMin) | (f > sizeThreshMax)
        m_label(find(m_label == i)) = 0;
    end
end
figure()
imshow(m_label);

[m_clean, n] = bwlabel(m_label);
for j = 1:n
    center(j, 2) = mean(mod(find(m_clean == j), size(img,1)));
    center(j, 1) = mean(find(m_clean == j) / size(img,1));
end