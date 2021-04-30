using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class Colony
{
    public int id;
    public string name;
    public Color color;

    public Colony(int id, string name, string color)
    {
        this.id = id;
        this.name = name;
        this.color = Utils.color.HexToColor(color);
    }
}
