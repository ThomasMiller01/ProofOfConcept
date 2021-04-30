using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class Colony
{    
    public string name;
    public Color color;

    public Colony(string name, string color)
    {        
        this.name = name;
        this.color = Utils.color.HexToColor(color);
    }
}
