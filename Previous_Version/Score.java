package Previous_Version;
public class Score {
    Photo photo1;
    Photo photo2;
    int score;

    public Score(Photo photo1, Photo photo2, int score) {
        this.photo1 = photo1;
        this.photo2 = photo2;
        this.score = score;
    }
    
    public Photo getPhoto1() {
        return photo1;
    }

    public Photo getPhoto2() {
        return photo2;
    }

    public int getScore() {
        return score;
    }
    
}
