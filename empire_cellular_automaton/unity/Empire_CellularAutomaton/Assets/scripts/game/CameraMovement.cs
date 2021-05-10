using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMovement : MonoBehaviour {

    public Camera cam;
    public float zoomStep, zoomSmooth, minCamSize;
    private float maxCamSize;
    public SpriteRenderer mapRenderer;

    private float mapMinX, mapMaxX, mapMinY, mapMaxY;
    private Vector3 dragOrigin;
    private float targetZoom;

    private void Awake()
    {
        this.maxCamSize = this.cam.orthographicSize;
        this.targetZoom = this.cam.orthographicSize;

        Bounds bounds = this.CameraBounds(this.cam);
        Transform transform = cam.transform;

        this.mapMinX = transform.position.x - bounds.size.x / 2f;
        this.mapMaxX = transform.position.x + bounds.size.x / 2f;

        this.mapMinY = transform.position.y - bounds.size.y / 2f;
        this.mapMaxY = transform.position.y + bounds.size.y / 2f;
    }

    private void Update()
    {
        this.PanCamera();
        this.ZoomCamera();
    }

    private void PanCamera()
    {
        if (Input.GetMouseButtonDown(2))
        {
            this.dragOrigin = cam.ScreenToWorldPoint(Input.mousePosition);
        }

        if (Input.GetMouseButton(2))
        {
            Vector3 difference = this.dragOrigin - this.cam.ScreenToWorldPoint(Input.mousePosition);


            this.cam.transform.position = this.ClampCamera(this.cam.transform.position + difference);            
        }
    }

    private void ZoomCamera()
    {
        float scroll = Input.GetAxis("Mouse ScrollWheel");
        if (scroll != 0.0f)
        {
            this.targetZoom -= scroll * this.zoomStep * (this.targetZoom / 10);
            this.targetZoom = Mathf.Clamp(this.targetZoom, this.minCamSize, this.maxCamSize);
        }

        cam.orthographicSize = Mathf.MoveTowards(cam.orthographicSize, this.targetZoom, this.zoomSmooth * Time.deltaTime);

        this.cam.transform.position = this.ClampCamera(this.cam.transform.position);
    }

    private Vector3 ClampCamera(Vector3 targetPosition)
    {
        float camHeight = this.cam.orthographicSize;
        float camWidth = this.cam.orthographicSize * this.cam.aspect;

        float minX = this.mapMinX + camWidth;
        float maxX = this.mapMaxX - camWidth;
        float minY = this.mapMinY + camHeight;
        float maxY = this.mapMaxY - camHeight;

        float newX = Mathf.Clamp(targetPosition.x, minX, maxX);
        float newY = Mathf.Clamp(targetPosition.y, minY, maxY);

        return new Vector3(newX, newY, targetPosition.z);
    }

    private Bounds CameraBounds(Camera cam)
    {
        float screenAspect = (float)Screen.width / (float)Screen.height;
        float cameraHeight = cam.orthographicSize * 2;
        Bounds bounds = new Bounds(cam.transform.position, new Vector3(cameraHeight * screenAspect, cameraHeight, 0));
        return bounds;
    }
}
