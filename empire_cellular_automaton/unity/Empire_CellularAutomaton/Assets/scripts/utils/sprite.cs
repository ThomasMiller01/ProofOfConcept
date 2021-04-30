using System.Collections;
using System.Collections.Generic;
using UnityEngine;

namespace Utils
{
    public class sprite
    {
        public static Sprite createSprite(Texture2D texture)
        {
            return Sprite.Create(texture, new Rect(new Vector2(0, 0), new Vector2(texture.width, texture.height)), new Vector2(0.5f, 0.5f));
        }

        public static void setSprite(GameObject gameObject, Sprite sprite)
        {
            gameObject.GetComponent<SpriteRenderer>().sprite = sprite;
        }

        public static Sprite getSprite(GameObject gameObject)
        {
            return gameObject.GetComponent<SpriteRenderer>().sprite;
        }
    }
}
