from vector import Vector3

class Bat:

    def __init__(self, x=0, y=0, z=0, dx=0, dy=0, dz=0, r=0, g=0, b=0):
	self.center = Vector3(x,y,z)
	self.velocity = Vector3(dx,dy,dz)
	self.color = Vector3(r,g,b)

    def prepare_update(self, flock):
	average_center = Vector3(0.,0.,0.)
	for f in flock:
	    if f == self:
	    	continue
	    average_center += f.center

	average_center /= len(flock) - 1
	self.updated_velocity = average_center - self.center
	self.updated_velocity.normalize()

    def apply_update(self):
	self.center += self.velocity
	self.velocity = self.updated_velocity

    def getCenter(self):
	return self.center.toList()

    def getColor(self):
	return self.color.toList()

    def getVelocity(self):
	return self.velocity.toList()
