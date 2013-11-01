/* *************************************************************
 *  
 *   Active Particles on Curved Spaces (APCS)
 *   
 *   Author: Rastko Sknepnek
 *  
 *   Division of Physics
 *   School of Engineering, Physics and Mathematics
 *   University of Dundee
 *   
 *   (c) 2013
 *   
 *   This program cannot be used, copied, or modified without
 *   explicit permission of the author.
 * 
 * ************************************************************* */

/*!
 * \file constraint_plane.cpp
 * \author Rastko Sknepnek, sknepnek@gmail.com
 * \date 31-Oct-2013
 * \brief Implementation of the planar constraint
 */ 

/*! Force all particles to be confined to the surface of the xy plane 
 *  by setting z = 0, vz = 0, fz = 0
 *  \param p particle to project onto the sphere
 */
void ConstraintPlane::enforce(Particle& p)
{
  bool periodic = m_system->get_periodic();
  double xlo = -0.5*m_lx, xhi = 0.5*m_lx;
  double ylo = -0.5*m_ly, yhi = 0.5*m_ly;
  double zlo = -0.5*m_lz, zhi = 0.5*m_lz;
  p.z = 0.0;
  p.vz = 0.0;
  p.fz = 0.0;
  // Check periodic boundary conditions 
  if (periodic)
  {
    if (p.x < xlo) p.x += m_lx;
    else if (p.x > xhi) p.x -= m_lx;
    if (p.y < ylo) p.y += m_ly;
    else if (p.y > yhi) p.y -= m_ly;
    if (p.z < zlo) p.z += m_lz;
    else if (p.z > zhi) p.z -= m_lz;
  }
}

/*! Rotate velocity vector of a particle around the normal vector (z axis)
 *  \note This function assumes that the particle has already been
 *  projected onto the plane and that its velocity is also in plane
 *  \param p Particle whose velocity to rotate
 *  \param phi angle by which to rotate it
*/
void ConstraintPlane::rotate_velocity(Particle& p, double phi)
{
  // Sine and cosine of the rotation angle
  double c = cos(phi), s = sin(phi);
  // Rotation matrix around z axis
  double Rxx = c, Rxy = -s;
  double Ryx = s, Ryy = c;
  // Apply rotation matrix
  double vx = Rxx*p.vx + Rxy*p.vy;
  double vy = Ryx*p.vx + Ryy*p.vy;
  // Update particle velocity
  p.vx = vx;
  p.vy = vy;
}