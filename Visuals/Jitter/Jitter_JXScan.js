/*

Scan a jiven directory for JXS files and populate a flexible menu.
When a function is chosen, populate its parameters dynamically.

*/

outlets = 13;
setoutletassist(12,"vect_index");
setoutletassist(11,"vect_num");
setoutletassist(10,"tex1_on_off");
setoutletassist(9,"param num");
setoutletassist(8,"param default4");
setoutletassist(7,"param default3");
setoutletassist(6,"param default2");
setoutletassist(5,"param default1");
setoutletassist(4,"done");
setoutletassist(3,"param type");
setoutletassist(2,"param name");
setoutletassist(1,"file size (in bytes)");
setoutletassist(0,"file name");
var j=1;
var paramnum=1;

function anything()
{
    var f = new Folder(messagename);
    f.reset();
    while (!f.end) {
        var thefile = new File(f.pathname + "/" + f.filename);
        if (thefile.isopen) {
            outlet(1,thefile.eof);
            thefile.close();
        } else {
            outlet(1,0);
        }
        outlet(0,f.filename);
        f.next();
    }
    f.close();
}

function recurseJXS(m)
{
    j=1;
    recursefiles(m);
}

function recursefiles(p)
{
    var f = new Folder(p);
    f.reset();
    i=1;
    while (!f.end) {
        var thefile = new File(f.pathname + "/" + f.filename);
        if (thefile.isopen) {
            outlet(1,thefile.eof);
            thefile.close();
        } else {
            outlet(1,0);
        }
        if (f.filetype == "fold") {
            new_file = f.pathname + "/" + f.filename;
            recursefiles(new_file)
        } else {
            if(f.filename.length > 0) {
                if (f.extension.match(/jxs/)) {                
                    outlet(0,f.filename);
                    i++;
                    j++;
                    outlet(1,j);
                } 
            }
        }
        f.next();
    }
    f.close();
    outlet(4,1);
}

function scanJXSfile(s)
{
    var f = new File(s);
    var i,a,c;

    if (f.isopen) {
        c = f.eof;
        while (i!=c) {
            new_word = f.readstring();
        i = f.position;
            post("string at fileposition[" + i + "]: " + new_word + "\n");
        }
        f.close();
    } else {
        post("could not open file: " + s + "\n");
    }
}

function scanJXSparam(r)
{
    var f = new File(r);
    var i,a,c,b,out,s,nm,tp,tpn;
    var found=0;
    var tex1_on_off=0;
    var type="";
    var n=1;
    var vect_num=0;
    var vect_index;

    if (f.isopen) {
        c = f.eof;
    for (i=0;i<c;i++) {
        a = f.readchars(1); //returns an array of single character strings
        if (a != " ") {
            if (a != "\t") {
                b = b + a;
            } else {
                if (found == 1) {
                    if (b.match(/name/)) {
                        s=b.replace(/name=/,"");
                        s=s.replace(/\"/,"");
                        s=s.replace(/\"/,"");
                        nm=s;
                        if (b.match(/tex1/)){
                            tex1_on_off=1;
                        }
                    }
                    if (b.match(/type/)) {
                        type=b;
                        if (type.match(/int/)) {
                            tpn=2;
                        }
                        if (type.match(/float/)) {
                            tpn=1;
                        }
                        if (type.match(/vec4/)) {
    /*                        tpn=4;
    */
                            tpn=1;
                        }
                        if (type.match(/vec2/)) {
                            tpn=1;
                        }
                        if (type.match(/vec3/)) {
                            tpn=1;
                        }
                        s=b.replace(/type=/,"");
                        tp=s;
                    }
                    if (b.match(/default/)) {
                        if (type.match(/vec4/)) {
                            vect_num++;
                            vect_index=1;
                            if (n == 1) {
                                n=4;
                            } 
                        } else if (type.match(/int/)) {
                                found = 0;
                            } else if (type.match(/float/)) {
                                    found = 0;
                                } 
                        s=b.replace(/default=/,"");
                        s=s.replace(/\"\>/,"");
                        s=s.replace(/\"/,"");
                        cvs=parseFloat(s);
                        outlet(12,vect_index);
                        outlet(11,vect_num);
                        outlet(9,paramnum);
                        outlet(5,cvs);
                        outlet(3,tpn);
                        outlet(2,nm);
                        paramnum++;
                    } else if (n > 1) {
                            n = n - 1;
                            vect_index++;
                            out = 5 + (4 - n); 
                            s=b.replace(/\"\>/,"");
                            s=s.replace(" ","");
                            cvs=parseFloat(s);
                            outlet(12,vect_index);
                            outlet(11,vect_num);
                            outlet(9,paramnum);
                            outlet(out,cvs);
                            outlet(3,tpn);
                            outlet(2,nm);
                            paramnum++;
                        }
                }
                if (b == "<param") {
                    found = 1;
                }
                b = "";
            }
        } else {
            if (found == 1) {
                if (b.match(/name/)) {
                    s=b.replace(/name=/,"");
                    s=s.replace(/\"/,"");
                    s=s.replace(/\"/,"");
                    nm=s;
                    if (b.match(/tex1/)){
                        tex1_on_off=1;
                    }
                }
                if (b.match(/type/)) {
                    type=b;
                    if (type.match(/int/)) {
                        tpn=2;
                    }
                    if (type.match(/float/)) {
                        tpn=1;
                    }
                    if (type.match(/vec4/)) {
/*                        tpn=4;
*/
                        tpn=1;
                    }
                    if (type.match(/vec2/)) {
                        tpn=1;
                    }
                    if (type.match(/vec3/)) {
                        tpn=1;
                    }
                    s=b.replace(/type=/,"");
                    tp=s;
                }
                if (b.match(/default/)) {
                    if (type.match(/vec4/)) {
                        vect_num++;
                        vect_index=1;
                        if (n == 1) {
                            n=4;
                        } 
                    } else if (type.match(/int/)) {
                            found = 0;
                        } else if (type.match(/float/)) {
                                found = 0;
                            } 
                    s=b.replace(/default=/,"");
                    s=s.replace(/\"\>/,"");
                    s=s.replace(/\"/,"");
                    cvs=parseFloat(s);
                    outlet(12,vect_index);
                    outlet(11,vect_num);
                    outlet(9,paramnum);
                    outlet(5,cvs);
                    outlet(3,tpn);
                    outlet(2,nm);
                    paramnum++;
                } else if (n > 1) {
                        n = n - 1;
                        vect_index++;
                        out = 5 + (4 - n); 
                        s=b.replace(/\"\>/,"");
                        s=s.replace(" ","");
                        cvs=parseFloat(s);
                        outlet(12,vect_index);
                        outlet(11,vect_num);
                        outlet(9,paramnum);
                        outlet(out,cvs);
                        outlet(3,tpn);
                        outlet(2,nm);
                        paramnum++;
                    }
            }
            if (b == "<param") {
                found = 1;
            }
            b = "";
        }
    }
        f.close();
    if (paramnum < 17) {
            while (paramnum!=17) {
            outlet(9,paramnum);
            outlet(5,0);    
            outlet(3,0);
            outlet(2,"none");    
            paramnum++;
        }
    }
        paramnum=1;
    outlet(10,tex1_on_off);
    } else {
        post("could not open file: " + s + "\n");
    }
}