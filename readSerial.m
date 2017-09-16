s = serial('COM4', 'BaudRate', 9600);
disp(s);

fopen(s);
fread(s)
%data=fscanf(s)
%y=str2double(data);
%disp(y);
fclose(s);