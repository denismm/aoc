H = 900000000000;
R = 5000000000000;

module hailstone(pos, dir, co, t) {
    b = acos(dir[2]/norm(dir));
    c = atan2(dir[1],dir[0]);
    color(co) translate(pos) {
        rotate([0, b, c]) {
            cylinder(h=H * norm(dir), r=R);
            sphere(r=2*R);
        }
        translate(dir * t) sphere(r=3*R);
    }
}

estimate = [177440926638, 403659059999, 673879641858, 1008197654002];

hailstone([331197478571816, 419588808460341, 308994415019000], [-91, -24, -6], "red", estimate[3]);
hailstone([330866855164228, 209537825210093, 231185943543128], [-150, -212, 72], "yellow", estimate[0]);
hailstone([328989866463373, 203709410146568, 262849170484878], [-105, 72, -7], "green", estimate[1]);
hailstone([231834394469732, 93189176593161, 440265961238428], [50, 315, -239], "blue", estimate[2]);