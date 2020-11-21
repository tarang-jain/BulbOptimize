. ./conf

echo '##############################'
echo "List of parameters for run"
cat ./conf
echo '##############################'

echo "Running Genetic Algorithm for Optimisation of bulb positions"

python3 ../../../GA.py --num_grid_points=$GridSize --num_iter=$NumIter\
 --intensity_lim=$IntensityLim --penalty_stiffness=$PenaltyStiffness $power_conf
