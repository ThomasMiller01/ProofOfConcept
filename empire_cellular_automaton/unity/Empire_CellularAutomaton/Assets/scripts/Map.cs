using System.Collections;
using System.Collections.Generic;
using UnityEngine;

using Utils;

public class Map : MonoBehaviour {

    public Texture2D map_texture;

    public Color32 land;
    public Color32 water;

    public Settings settings;    

    [System.NonSerialized]
    public Vector2 dimensions;

    [System.NonSerialized]
    public Color32[] map_pixels;

    [System.NonSerialized]
    public Color32[] original_map_pixels;

    [System.NonSerialized]
    SpriteRenderer spriteRenderer;

    void Start()
    {        
        this.spriteRenderer = this.gameObject.GetComponent<SpriteRenderer>();
        this.spriteRenderer.sprite = Utils.sprite.createSprite(this.map_texture);
    }

    public void loadTexture()
    {        
        this.original_map_pixels = this.map_texture.GetPixels32();
        this.map_pixels = (Color32[])this.original_map_pixels.Clone();

        this.dimensions = new Vector2(this.map_texture.width, this.map_texture.height);                
    }

    public void draw(Dictionary<Vector2, HashSet<Person>> people)
    {        
        Texture2D texture = new Texture2D((int)this.dimensions.x, (int)this.dimensions.y);

        texture.filterMode = FilterMode.Point;

        if (this.settings.EraseLastPos)
        {
            this.map_pixels = (Color32[])this.original_map_pixels.Clone();
        }

        foreach(HashSet<Person> value in people.Values)
        {
            foreach(Person person in value)
            {
                this.map_pixels[Utils.datastructure.convert2dto1d(person.pos, (int)this.dimensions.x)] = person.colony.color;
                break;
            }
        }            

        texture.SetPixels32(this.map_pixels);        
        
        texture.Apply();                

        this.spriteRenderer.sprite = Utils.sprite.createSprite(texture);        
    }    

    public Color getPixel(Vector2 pos)
    {
        return this.map_pixels[Utils.datastructure.convert2dto1d(pos, (int)this.dimensions.x)];
    }
}
