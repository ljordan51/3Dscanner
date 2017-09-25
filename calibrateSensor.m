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
legend2 = strcat("best fit curve - order ", int2str(order));
legend('experimental data', legend2);
xlabel('sensor value')
ylabel('distance (cm)')