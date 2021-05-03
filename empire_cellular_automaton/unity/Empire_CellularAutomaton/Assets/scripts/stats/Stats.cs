using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class Stats : MonoBehaviour {
    
    public GameManager gameManager;

    public Text generation;
    public Text people;
    public Text colonies;

    // Update is called once per frame
    void Update () {
        // generation
        string generation_text = "Gen [" + this.gameManager.generation.ToString() + "], Year [" + this.gameManager.year.ToString() + "], Day [" + this.gameManager.day.ToString() + "]";
        this.generation.text = generation_text;

        int population = 0;        
        
        string colonies_text = "";
        Dictionary<string, int> colonies_dict = new Dictionary<string, int>();                

        foreach(ColonySettings colony in this.gameManager.settings.colonies)
        {
            colonies_dict[colony.name] = 0;            
        }

        foreach(var item in this.gameManager.people)
        {
            foreach (Person person in item.Value)
            {
                colonies_dict[person.colony.name]++;
                population++;
            }
        }

        this.people.text = "Population: " + population.ToString();

        foreach (var colony in colonies_dict)
        {
            colonies_text += colony.Key + ": " + colony.Value.ToString() + "\n";
        }
        this.colonies.text = colonies_text;
    }
}
