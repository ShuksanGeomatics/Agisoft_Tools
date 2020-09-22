#compatibility PhotoScan Pro 1.3.1
#creates footprint shape layer in the active chunk

import PhotoScan

doc = PhotoScan.app.document
chunk = doc.chunk

if not chunk.shapes:
	chunk.shapes = PhotoScan.Shapes()
	chunk.shapes.crs = chunk.crs
T = chunk.transform.matrix
footprints = chunk.shapes.addGroup()
footprints.label = "Footprints"
footprints.color = (30, 239, 30)

if chunk.dense_cloud:
	surface = chunk.dense_cloud
elif chunk.model:
	surface = chunk.model
else:
	surface = chunk.point_cloud

for camera in chunk.cameras:
	if not camera.transform:
		continue #skipping NA cameras
	
	sensor = camera.sensor
	corners = list()
	for i in [[0, 0], [sensor.width - 1, 0], [sensor.width - 1, sensor.height - 1], [0, sensor.height - 1]]:
		corners.append(surface.pickPoint(camera.center, camera.transform.mulp(sensor.calibration.unproject(PhotoScan.Vector(i)))))
		if not corners[-1]:
			corners[-1] = chunk.point_cloud.pickPoint(camera.center, camera.transform.mulp(sensor.calibration.unproject(PhotoScan.Vector(i))))
		if not corners[-1]:
			break
		corners[-1] = chunk.crs.project(T.mulp(corners[-1]))
		
	if not all(corners):
		print("Skipping camera " + camera.label)
		continue
		
	if len(corners) == 4:
		shape = chunk.shapes.addShape()
		shape.label = camera.label
		shape.attributes["Photo"] = camera.label
		shape.type = PhotoScan.Shape.Type.Polygon
		shape.group = footprints
		shape.vertices = corners
		shape.has_z = True
		
PhotoScan.app.update()
print("Script finished")