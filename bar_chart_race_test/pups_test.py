import bar_chart_race as bcr
import pandas as pd
video_path = "/Users/huyiqing/Movies/py4v/pups.mp4"
pups_df = pd.read_csv("/bar_chart_race_test/puppy_weights.csv").set_index('Date')
pups_df.interpolate(axis=0,inplace=True)
print(pups_df.tail(10))

saved_flag = bcr.bar_chart_race(pups_df.head(30),
                  filename=video_path,

                  orientation='h',
                  title='Puppy Weights (g)',
                  tick_image_mode='trailing',
                img_label_folder = '/Users/huyiqing/Movies/assets/pups',
)
print(saved_flag)
print(f"视频已保存到: {video_path}")