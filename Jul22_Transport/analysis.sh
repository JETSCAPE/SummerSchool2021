TRANSPORT_WORKSHOP_FOLDER="../../SummerSchool2021/Jul22_Transport/"
RESULTS_FOLDER="./results/"
mkdir -p $RESULTS_FOLDER

python $TRANSPORT_WORKSHOP_FOLDER/quick_read.py smash_output/collisions_binary.bin

python ${TRANSPORT_WORKSHOP_FOLDER}/count_reactions.py --production ρ⁰ \
       ${RESULTS_FOLDER}/reaction_rates_output_midrapidity.txt \
       ${RESULTS_FOLDER}/production_output_midrapidity.txt \
       "π⁺,π⁻:ρ⁰|π⁺,ρ⁰:a₁(1260)⁺|π⁻,ρ⁰:a₁(1260)⁻|π⁰,ρ⁰:h₁(1170)|π⁰,ρ⁰:ω" \
       1.0  ${TRANSPORT_WORKSHOP_FOLDER}/dummy_config.yaml \
       ./smash_output/collisions_binary.bin
