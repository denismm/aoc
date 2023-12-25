H = 1000000000000000;
R = 5000000000000;
x = -91;
y = -24;
z = -6;
b = acos(z/norm([x,y,z]));
c = atan2(y,x);
translate([331197478571816, 419588808460341, 308994415019000])
    rotate([0, b, c]) {
        cylinder(h=H, r=R);
        sphere(r=2*R);
    }
        
x1 = -150;
y1 = -212;
z1 = 72;
b1 = acos(z1/norm([x1,y1,z1]));
c1 = atan2(y1,x1);
translate([330866855164228, 209537825210093, 231185943543128])
    rotate([0, b1, c1]) {
        cylinder(h=H, r=R);
        sphere(r=2*R);
    }
        
x2 = -105;
y2 = 72;
z2 = -7;
b2 = acos(z2/norm([x2,y2,z2]));
c2 = atan2(y2,x2);
translate([328989866463373, 203709410146568, 262849170484878])
    rotate([0, b2, c2]) {
        cylinder(h=H, r=R);
        sphere(r=2*R);
    }

x3 = 50;
y3 = 315;
z3 = -239;
b3 = acos(z3/norm([x3,y3,z3]));
c3 = atan2(y3,x3);
translate([231834394469732, 93189176593161, 440265961238428])
    rotate([0, b3, c3]) {
        cylinder(h=H, r=R);
        sphere(r=2*R);
    }
