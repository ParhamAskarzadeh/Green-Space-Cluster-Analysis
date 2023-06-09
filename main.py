import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class KmeansAlgorythm:
    def __initialize_centroids(self, points, k):
        centroids = points.copy()
        np.random.shuffle(centroids)
        return centroids[:k]

    def __closest_centroid(self, points, centroids):
        distances = np.sqrt(((points - centroids[:, np.newaxis]) ** 2).sum(axis=2))
        return np.argmin(distances, axis=0)

    def __move_centroids(self, points, closest, centroids):
        return np.array([points[closest == k].mean(axis=0) for k in range(centroids.shape[0])])

    def run(self, points, k, max_iterations=100):
        centroids = self.__initialize_centroids(points, k)
        for _ in range(max_iterations):
            closest = self.__closest_centroid(points, centroids)
            centroids = self.__move_centroids(points, closest, centroids)
        return closest


class Plot:
    def create_plot(self, dataset, colors):
        teams = dataset['team_number'].unique()
        for team in teams:
            team_points = dataset[dataset['team_number'] == team]
            plt.scatter(team_points['feature_1'], team_points['feature_2'], color=colors[team],
                        label=f'Team {team + 1}')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('City map')
        plt.legend()
        plt.show()


if __name__ == '__main__':
    kmeans_algorythm = KmeansAlgorythm()
    dataset = pd.read_csv('rc_task_2.csv')
    team_numbers = kmeans_algorythm.run(dataset[['feature_1', 'feature_2']].values, 5)
    dataset['team_number'] = team_numbers
    dataset.to_csv('final_dataset.csv', index=False)
    plot = Plot()
    plot.create_plot(dataset, ['red', 'blue', 'green', 'orange', 'purple'])
