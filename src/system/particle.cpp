/* *************************************************************
 *  
 *   Soft Active Mater on Surfaces (SAMoS)
 *   
 *   Author: Rastko Sknepnek
 *  
 *   Division of Physics
 *   School of Engineering, Physics and Mathematics
 *   University of Dundee
 *   
 *   (c) 2013, 2014
 * 
 *   School of Science and Engineering
 *   School of Life Sciences 
 *   University of Dundee
 * 
 *   (c) 2015
 * 
 *   Author: Silke Henkes
 * 
 *   Department of Physics 
 *   Institute for Complex Systems and Mathematical Biology
 *   University of Aberdeen  
 * 
 *   (c) 2014, 2015
 *  
 *   This program cannot be used, copied, or modified without
 *   explicit written permission of the authors.
 * 
 * ************************************************************* */

/*!
 * \file particle.cpp
 * \author Rastko Sknepnek, sknepnek@gmail.com
 * \date 16-Oct-2013
 * \brief Auxiliary functions for Particle class
 */ 

#include "particle.hpp"

ostream& operator<<(ostream& out, const Particle& p)
{
  out << "-------- PARTICLE ------------" << endl;
  out << format("id : %d\n") % p.get_id()     
  << format("flag : %d\n") % p.get_flag()
  << format("type : %d\n") % p.get_type()
  << format("radius : %15.9e\n") % p.get_radius()       
  << format("age : %15.9e\n") % p.age       
  << format("(x,y,z) : (%15.9e,%15.9e,%15.9e)\n") % p.x % p.y % p.z
  << format("(vx,vy,vz) : (%15.9e,%15.9e,%15.9e)\n") % p.vx % p.vy % p.vz
  << format("(nx,ny,nz) : (%15.9e,%15.9e,%15.9e)\n") % p.nx % p.ny % p.nz
  << format("(nvx,nvy,nvz) : (%15.9e,%15.9e,%15.9e)\n") % p.Nx % p.Ny % p.Nz
  << format("(fx,fy,fz) : (%15.9e,%15.9e,%15.9e)\n") % p.fx % p.fy % p.fz
  << format("omega : %15.9e\n") % p.omega
  << format("coordination : %d\n") % p.coordination
  << format("native cell area : %d\n") % p.A0
  << format("groups : ");
  for (list<string>::const_iterator it = p.groups.begin(); it != p.groups.end(); it++)
    out << format(" %s ") % (*it);
  if (p.bonds.size() > 0)
  {
    out << endl << format("bonds : ");
    for (vector<int>::const_iterator it_b = p.bonds.begin(); it_b != p.bonds.end(); it_b++)
      out << format(" %d ") % (*it_b);
  }
  if (p.angles.size() > 0)
  {
    out << endl << format("angles : ");
    for (vector<int>::const_iterator it_a = p.angles.begin(); it_a != p.angles.end(); it_a++)
      out << format(" %d ") % (*it_a);
  }
  out << endl;
  out << "----------------------------";
  out << endl;
  return out;
}