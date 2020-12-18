# 

#### Write multiple week's data
    for i in `seq 1 16`; do py main.py week $i; done



### Advanced Passing Data Columns:
    player, player_id, team, pass_cmp, pass_att, pass_yds, pass_first_down, pass_first_down_pct, pass_target_yds, pass_tgt_yds_per_att, pass_air_yds, pass_air_yds_per_cmp, pass_air_yds_per_att, pass_yac, pass_yac_per_cmp, pass_drops, pass_drop_pct, pass_poor_throws, pass_poor_throw_pct, pass_sacked, pass_blitzed, pass_hurried, pass_hits, rush_scrambles, rush_scrambles_yds_per_att

#### Write Headers to new Passing Data Files:
    for f in data-2019/*passing*; do echo $f; echo "player,player_id,team,pass_cmp,pass_att,pass_yds,pass_first_down,pass_first_down_pct,pass_target_yds,pass_tgt_yds_per_att,pass_air_yds,pass_air_yds_per_cmp,pass_air_yds_per_att,pass_yac,pass_yac_per_cmp,pass_drops,pass_drop_pct,pass_poor_throws,pass_poor_throw_pct,pass_sacked,pass_blitzed,pass_hurried,pass_hits,rush_scrambles,rush_scrambles_yds_per_att" >> $f; done


### Advanced Rushing Data Columns:
    player,player_id,team,rush_att,rush_yds,rush_first_down,rush_yds_before_contact,rush_yds_bc_per_rush,rush_yac,rush_yac_per_rush,rush_broken_tackles,rush_broken_tackles_per_rush

### Advanced Receiving Data Columns:
    player, player_id, team, targets, rec, rec_yds, rec_first_down, rec_air_yds, rec_air_yds_per_rec, rec_yac, rec_yac_per_rec, rec_broken_tackles, rec_broken_tackles_per_rec, rec_drops, rec_drop_pct

