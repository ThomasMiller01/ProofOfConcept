using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Stats : MonoBehaviour {
    
    public GameManager gameManager;

    public Text people;
    public Text colonies;

    // Update is called once per frame
    void Update () {
        int total_people = gameManager.people.Count;
        people.text = "Total: " + total_people.ToString();

        string colonies_text = "";
        Dictionary<string, int> colonies_dict = new Dictionary<string, int>();                

        foreach(ColonySettings colony in gameManager.settings.colonies)
        {
            colonies_dict[colony.name] = 0;            
        }

        foreach (Person person in gameManager.people)
        {
            colonies_dict[person.colony.name]++;
        }

        foreach(var colony in colonies_dict)
        {
            colonies_text += colony.Key + ": " + colony.Value.ToString() + "\n";
        }
        colonies.text = colonies_text;
    }
}
