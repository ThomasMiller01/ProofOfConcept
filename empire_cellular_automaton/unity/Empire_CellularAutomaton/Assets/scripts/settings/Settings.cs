using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Settings : MonoBehaviour {
    public int days;
    public int years;
    public int reproductionThreshold;    
    public Vector2 strength;

    public int maxBirthCount;

    public bool EraseLastPos;
    public bool mutations;
    public bool staticPopulation;

    public ColonySettings[] colonies;    
}
