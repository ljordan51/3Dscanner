clear
close all

order = 4;
distances = [15, linspace(20,120,11)];
sensorVals = [563, 535, 423, 320, 258, 213, 184, 160, 149, 132, 120, 111];

plot(sensorVals, distances);

coeffs = polyfit(sensorVals, distances, order);
calDistances = zeros(1,length(sensorVals));

for i = 1:length(coeffs)
    power = length(coeffs)-i;
    calDistances = calDistances + coeffs(i).*sensorVals.^power;
end

hold on
plot(sensorVals, calDistances);
legend2 = strcat("Best Fit Curve - Order ", int2str(order));
legend('Experimental Data', legend2);
xlabel('Sensor Value');
ylabel('Distance (cm)');
title(strcat("Polyfit and Experimental Data Comparison - Order ", int2str(order)));
grid on;
axis([0,600,0,130]);

figure
plot(distances,sensorVals/1023*5);
title('Analog Voltage vs. Actual Distance');
ylabel('Analog Voltage (V)');
xlabel('Actual Distance (cm)');
axis([0,130,0,3]);
grid on;