// popu.js
//
// simulates the logistic population equation:
// f(x) = rx(1-x)
// 
// input is r.  output is current x.
//
// rld, 5.04
//

// inlets and outlets
inlets = 1;
outlets = 10;

// global variables

// float -- run the equation once
function msg_int(r)
{

switch (true) {
    case (r >= 0 && r <= 10 ):
        outlet(0,r);
        break;
    case (r >= 11 && r <= 20):
        outlet(1,r-10);
        break;
    case (r >= 21 && r <= 30):
        outlet(2,r-20);
        break;
    case (r >= 31 && r <= 40):
        outlet(3,r-30);
        break;
    case (r >= 41 && r <= 50):
        outlet(4,r-40);
        break;
    case (r >= 51 && r <= 60):
        outlet(5,r-50);
        break;
    case (r >= 61 && r <= 70):
        outlet(6,r-60);
        break;
    case (r >= 71 && r <= 80):
        outlet(7,r-70);
        break;
    case (r >= 81 && r <= 90):
        outlet(8,r-80);
        break;
    case (r >= 91 && r <= 100):
        outlet(9,r-90);
        break;
}
}

