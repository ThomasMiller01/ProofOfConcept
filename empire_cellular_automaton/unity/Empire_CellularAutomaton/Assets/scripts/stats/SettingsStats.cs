using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SettingsStats : MonoBehaviour {

    public Text loopText;
    public Text reproductionText;
    public Text maxBirthCountText;
    public Text strengthText;

    public Settings settings;	
		
	void Update () {
        this.loopText.text = "1 gen := " + this.settings.years + " years\n1 year := " + this.settings.days + " days";

        this.reproductionText.text = "ReproductionThreshold: " + this.settings.reproductionThreshold;

        this.maxBirthCountText.text = "MaxBirthCount: " + this.settings.maxBirthCount;

        this.strengthText.text = "Strength: [" + this.settings.strength.x + ", " + this.settings.strength.y + "]";
	}
}
