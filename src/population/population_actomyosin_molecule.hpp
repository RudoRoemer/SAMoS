/* ***************************************************************************
 *
 *  Copyright (C) 2013-2016 University of Dundee
 *  All rights reserved. 
 *
 *  This file is part of SAMoS (Soft Active Matter on Surfaces) program.
 *
 *  SAMoS is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  SAMoS is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * ****************************************************************************/

/*!
 * \file population_actomyosin_molecule.hpp
 * \author Rastko Sknepnek, sknepnek@gmail.com
 * \date 18-Oct-2016
 * \brief Declaration of PopulationActomyosinMolecule class.
 */ 

#ifndef __POPULATION_ACTOMYOSIN_MOLECULE_HPP__
#define __POPULATION_ACTOMYOSIN_MOLECULE_HPP__

#include <list>
#include <stdexcept>
#include <cmath>

#include "population.hpp"
#include "rng.hpp"


using std::list;
using std::runtime_error;
using std::sqrt;
using std::exp;

/*! PopulationActomyosinMolecule class handles unbinding of the entire myosin
 *  molecule form the rest of the system. If any of the beads is in the attached state 
 *  all head groups detach. This detachment is done with a given probability.
 *  This is to model experiments of Christoph Schmidt.
 *
*/
class PopulationActomyosinMolecule : public Population
{
public:
  
  //! Construct PopulationActomyosinMolecule object
  //! \param sys Reference to the System object
  //! \param msg Reference to the system wide messenger
  //! \param param Reference to the parameters that control given population control
  PopulationActomyosinMolecule(SystemPtr sys, const MessengerPtr msg, pairs_type& param) : Population(sys,msg,param)
  { 
    if (param.find("seed") == param.end())
    {
      m_msg->msg(Messenger::WARNING,"Actomyosin molecule population control. No random number generator seed specified. Using default 0.");
      m_rng = make_shared<RNG>(0);
      m_msg->write_config("population.actomyosin_molecule.seed",lexical_cast<string>(0));
    }
    else
    {
      m_msg->msg(Messenger::INFO,"Actomyosin population control. Setting random number generator seed to "+param["seed"]+".");
      m_rng = make_shared<RNG>(lexical_cast<int>(param["seed"]));
      m_msg->write_config("population.actomyosin_molecule.seed",param["seed"]);
    }
    
    if (param.find("detachment_rate") == param.end())
    {
      m_msg->msg(Messenger::WARNING,"Actomyosin molecule population control. No detachment rate per particle set. Using default 0.1.");
      m_detach_rate = 0.1;
    }
    else
    {
      m_msg->msg(Messenger::INFO,"Actomyosin molecule population control. Setting detachment rate per particle "+param["detachment_rate"]+".");
      m_detach_rate = lexical_cast<double>(param["detachment_rate"]);
    }
    m_msg->write_config("population.actomyosin_molecule.detachment_rate",lexical_cast<string>(m_detach_rate));
    
    if (param.find("detached_type") == param.end())
    {
      m_msg->msg(Messenger::WARNING,"Actomyosin molecule population control. No type of detached bead set. Using default 3.");
      m_type_d = 3;
    }
    else
    {
      m_msg->msg(Messenger::INFO,"Actomyosin molecule population control. Setting type of detached bead "+param["detached_type"]+".");
      m_type_d = lexical_cast<int>(param["detached_type"]);
    }
    m_msg->write_config("population.actomyosin_molecule.detached_type",lexical_cast<string>(m_type_d));
   
    if (param.find("attached_type") == param.end())
    {
      m_msg->msg(Messenger::WARNING,"Actomyosin molecule population control. No type of attachment bead set. Using default 4.");
      m_type_a = 4;
    }
    else
    {
      m_msg->msg(Messenger::INFO,"Actomyosin molecule population control. Setting type of attachment bead "+param["attached_type"]+".");
      m_type_a = lexical_cast<int>(param["attached_type"]);
    }
    m_msg->write_config("population.actomyosin_molecule.attached_type",lexical_cast<string>(m_type_a));

    if (param.find("actin_type") == param.end())
    {
      m_msg->msg(Messenger::WARNING,"Actomyosin molecule population control. No type of actin bead set. Using default 1.");
      m_type_actin = 1;
    }
    else
    {
      m_msg->msg(Messenger::INFO,"Actomyosin molecule population control. Setting type of actin bead "+param["actin_type"]+".");
      m_type_actin = lexical_cast<int>(param["actin_type"]);
    }
    m_msg->write_config("population.actomyosin_molecule.actin_type",lexical_cast<string>(m_type_actin));  
    if (m_detach_rate*m_freq*m_system->get_integrator_step() > 1.0)
      m_msg->msg(Messenger::WARNING,"Actomyosin molecule population control. Detachment rate per particle is too high. Particles will always detach.");
  }
  
  //! This function controls attachment (note: function name derives from the initial intent of the population classes to use to treat cell division)
  void divide(int);
  
  //! This function controls detachment
  void remove(int) { }
  
  //! Not used here
  void add(int t) { }
  
  //! Not used here 
  void grow(int time) { }
  
  //! Not used here
  void elongate(int time) { }
  
  
private:
  
  RNGPtr m_rng;                  //!< Actomyosin number generator
  double m_detach_rate;          //!< Rate of detachment, defined per particle
  int m_type_d;                  //!< Type when detached
  int m_type_a;                  //!< Type when attached
  int m_type_actin;              //!< Type of the actin beads

};

typedef shared_ptr<PopulationActomyosinMolecule> PopulationActomyosinMoleculePtr;

#endif
