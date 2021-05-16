using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class ColonySettings : MonoBehaviour {    
    public int id;
    public new string name;
    public string color;
    public int number_of_people;
    public Vector2 start;

    public GameObject map;

    public void OnDrawGizmos()
    {
        Gizmos.color = Utils.color.HexToColor(color);

        Vector2 screenPos = Utils.pixels.WorldToScreen(this.map, this.start);

        Gizmos.DrawSphere(new Vector3(screenPos.x, screenPos.y), 5f);
    }
}
