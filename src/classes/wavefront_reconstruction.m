clear all
clf
cla

set(gcf, 'Position', [100, 100, 1700, 800]);

x = linspace(-1, 1,1000);
y = linspace(-1,1,1000);

[XX YY] = meshgrid(x,y);

mask = (XX).^2 + (YY).^2 <= 1;

%% Input
% Zernike 14 coefficients (Piston ignored)
coef = [
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
0	0
];

coef_in = coef(:,1);

coef_out = coef(:,2);
    
PM_in(:,:,1) = XX;
PM_in(:,:,2) = YY;
PM_in(:,:,3) = 2*XX.*YY;
PM_in(:,:,4) = -1 + 2*YY.^2 + 2*XX.^2;
PM_in(:,:,5) = YY.^2 - XX.^2;
PM_in(:,:,6) = 3*XX.*YY.^2 - XX.^3;
PM_in(:,:,7) = -2*XX + 3*XX.*YY.^2 + 3*XX.^3;
PM_in(:,:,8) = -2*YY + 3*YY.^3 + 3*XX.^2*YY;
PM_in(:,:,9)= YY.^3 - 3*XX.^2.*YY;
PM_in(:,:,10)= 4*YY.^3.*XX - 4*XX.^3.*YY;
PM_in(:,:,11)= -6*XX.*YY + 8*YY.^3.*XX + 8*XX.^3.*YY;
PM_in(:,:,12)= 1 - 6*YY.^2 - 6*XX.^2 + 6*YY.^4 + 12*XX.^2*YY.^2 + 6*XX.^4;
PM_in(:,:,13)= -3*YY.^2 + 3*XX.^2 + 4*YY.^4 - 4*XX.^2.*YY.^2 - 4*XX.^4;
PM_in(:,:,14)= YY.^4 - 6*XX.^2.*YY.^2 + 4*XX.^4;

Wm_without_tilt_in = zeros(1000, 1000, 12);

for i = 3:length(coef_out)
    Wm_without_tilt_in(:,:,i-2) = PM_in(:,:,i)*coef_in(i);
end

Wm_in = sum(Wm_without_tilt_in,3);
%Piston = mean(Wm_without_tilt_in,'all');
Piston = (max(Wm_in(:)) + min(Wm_in(:)))/2;
Wm_in = Wm_in -ones(length(XX))*Piston;
masked_Wm_in = Wm_in.* mask;
masked_Wm_in(mask == 0) = NaN;

% Create the subplot
subplot(2,3,1)
imagesc(x,y,masked_Wm_in)
axis xy
axis square
xlabel('\rho_x')
ylabel('\rho_y')
zlabel('µm')
title('Input Wavefront')
set(gca, 'FontSize', 18)
c = colorbar;
ylabel(c, 'µm')
colormap(jet)
caxis([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);


% 
% 
% % subplot(1,3,1)
% % surfc(XX,YY,masked_Wm_in,'EdgeColor','none','LineStyle','-','LineWidth',3)
% % 
% % axis xy
% % axis square
% % xlabel('\rho_x')
% % ylabel('\rho_y')
% % zlabel('z [µm]')
% % title('Reconstructed Wavefront')
% % set(gca, 'FontSize', 10)
% % d = colorbar;
% % ylabel(d, 'µm')
% % colormap(jet)
% 
%% Output

PM_out(:,:,1) = XX;
PM_out(:,:,2) = YY;
PM_out(:,:,3) = 2*XX.*YY;
PM_out(:,:,4) = -1 + 2*YY.^2 + 2*XX.^2;
PM_out(:,:,5) = YY.^2 - XX.^2;
PM_out(:,:,6) = 3*XX.*YY.^2 - XX.^3;
PM_out(:,:,7) = -2*XX + 3*XX.*YY.^2 + 3*XX.^3;
PM_out(:,:,8) = -2*YY + 3*YY.^3 + 3*XX.^2*YY;
PM_out(:,:,9)= YY.^3 - 3*XX.^2.*YY;
PM_out(:,:,10)= 4*YY.^3.*XX - 4*XX.^3.*YY;
PM_out(:,:,11)= -6*XX.*YY + 8*YY.^3.*XX + 8*XX.^3.*YY;
PM_out(:,:,12)= 1 - 6*YY.^2 - 6*XX.^2 + 6*YY.^4 + 12*XX.^2*YY.^2 + 6*XX.^4;
PM_out(:,:,13)= -3*YY.^2 + 3*XX.^2 + 4*YY.^4 - 4*XX.^2.*YY.^2 - 4*XX.^4;
PM_out(:,:,14)= YY.^4 - 6*XX.^2.*YY.^2 + 4*XX.^4;

Wm_without_tilt_out = zeros(1000, 1000, 12);

for i = 3:length(coef_out)
    Wm_without_tilt_out(:,:,i-2) = PM_out(:,:,i)*coef_out(i);
end

Wm_out = sum(Wm_without_tilt_out,3);
Piston_out = (max(Wm_out(:)) + min(Wm_out(:)))/2;
Wm_out = Wm_out -ones(length(XX)).*Piston;
masked_Wm_out = Wm_out.* mask;
masked_Wm_out(mask == 0) = NaN;

% Create the subplot
subplot(2,3,2)
imagesc(x,y,masked_Wm_out)
axis xy
axis square
xlabel('\rho_x')
ylabel('\rho_y')
zlabel('µm')
title('Reconstructed Wavefront')
set(gca, 'FontSize', 18)
c = colorbar;
ylabel(c, 'µm')
colormap(jet)
caxis([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);

%% Residual
residual = masked_Wm_in - masked_Wm_out;
subplot(2,3,3)
imagesc(x,y,residual)
axis xy
axis square
xlabel('\rho_x')
ylabel('\rho_y')
zlabel('µm')
title('Residual Wavefront')
set(gca, 'FontSize', 18)
c = colorbar;
ylabel(c, 'µm')
colormap(jet)
caxis([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);

% surface plot - Input
subplot(2,3,4)

surfc(XX,YY,masked_Wm_in,'EdgeColor','none','LineStyle','-','LineWidth',3)

axis xy
axis square
xlabel('\rho_x')
ylabel('\rho_y')
zlabel('z [µm]')
title('Input Wavefront')
set(gca, 'FontSize', 18)
c = colorbar;
ylabel(c, 'µm')
colormap(jet)
caxis([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);

% subplot reconstructed
subplot(2,3,5)

surfc(XX,YY,masked_Wm_out,'EdgeColor','none','LineStyle','-','LineWidth',3)

axis xy
axis square
xlabel('\rho_x')
ylabel('\rho_y')
zlabel('z [µm]')
title('Reconstructed Wavefront')
set(gca, 'FontSize', 18)
c = colorbar;
ylabel(c, 'µm')
colormap(jet)
caxis([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);

% subplot residual
subplot(2,3,6)

surfc(XX,YY,residual,'EdgeColor','none','LineStyle','-','LineWidth',3)

axis xy
axis square
xlabel('\rho_x')
ylabel('\rho_y')
zlabel('z [µm]')
title('Residual Wavefront')
set(gca, 'FontSize', 18)
c = colorbar;
ylabel(c, 'µm')
%zlim([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);
colormap(jet)
caxis([min(masked_Wm_in(:)), max(masked_Wm_in(:))]);