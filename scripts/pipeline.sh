#!/usr/bin/env bash

EVAL_DIR=misc/evaluations
CURR_DATE=$(date '+%Y%m%d')
CURR_EVAL_DIR=evaluation-$CURR_DATE
FULL_EVAL_DIR="$EVAL_DIR/$CURR_EVAL_DIR/test"


############################ Prompt ############################
CONFIG_750="$FULL_EVAL_DIR/config_750.json"
CONFIG_200="$FULL_EVAL_DIR/config_200.json"
CONFIG_50="$FULL_EVAL_DIR/config_50.json"

for CONFIG_FILE in $CONFIG_50 $CONFIG_200 $CONFIG_750
do
  echo $CONFIG_FILE
  python randomizer/run_randomizer.py --config $CONFIG_FILE
done

############################ Respond ###########################
PROMPT_JSON_750="$FULL_EVAL_DIR/random_prompts_750.json"
PROMPT_JSON_200="$FULL_EVAL_DIR/random_prompts_200.json"
PROMPT_JSON_50="$FULL_EVAL_DIR/random_prompts_50.json"

for PROMPT_JSON in $PROMPT_JSON_50 $PROMPT_JSON_200 $PROMPT_JSON_750
do
  echo "$PROMPT_JSON"
  python misc/response_generator.py "$PROMPT_JSON"
done

########################### Evaluate ###########################
for NUM_PROMPTS in '50' '200' '750'
do
  for RES_FILE in "$FULL_EVAL_DIR"/"$NUM_PROMPTS"/responses/*.csv
  do
    echo "Using responses at $RES_FILE"
    MODEL=${RES_FILE##*/}
    echo "Evaluating model $MODEL"
    python randomizer/evaluate_randomized_objects.py \
            --input "$FULL_EVAL_DIR/random_prompts_$NUM_PROMPTS.pkl" \
            --output "$FULL_EVAL_DIR/$NUM_PROMPTS/evaluations/evaluation_results_$MODEL" \
            --model_response "$RES_FILE" \
            --original_prompts "$FULL_EVAL_DIR/random_prompts_$NUM_PROMPTS.json"
  done
done
