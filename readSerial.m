s = serial('COM7', 'BaudRate', 9600);
%s.InputBufferSize = 6;
disp(s);
A = zeros(6,1);
temp = zeros(6,1)-1;

fopen(s);
fwrite(s,1);
while 1
    if s.BytesAvailable == 6
        temp = fread(s);
    end
    if temp(1) == 255
        break
    elseif temp(1) == -1
        continue
    else
        A = [A;temp];
    end
end
fclose(s);
disp('done');