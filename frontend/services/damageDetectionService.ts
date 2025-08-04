import { DamageAnalysis, DamageType, CostEstimation } from '@/types';

export class DamageDetectionService {
  private static readonly API_URL = 'http://localhost:8000/api';
  
  static async analyzeImage(imageUri: string, userId: string): Promise<DamageAnalysis> {
    try {
      // Create form data
      const formData = new FormData();
      // For web: use Blob
      const imageResponse = await fetch(imageUri);
      const imageBlob = await imageResponse.blob();
      formData.append('file', imageBlob, 'image.jpg');
      formData.append('user_id', userId);

      // Send request to backend
      const response = await fetch(`${this.API_URL}/analyze`, {
        method: 'POST',
        body: formData,
        headers: {
          'Accept': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error('Failed to analyze image');
      }

      const data = await response.json();
      return {
        id: data.id,
        userId: data.user_id,
        imageUri: data.image_path,
        analysisDate: new Date(data.analysis_date),
        damageDetected: data.damage_detected,
        severity: data.severity,
        confidence: data.confidence,
        status: 'Completed',
        damageType: data.analysis_data.damage_types || [],
        costEstimation: data.analysis_data.cost_estimation || {
          totalCost: 0,
          laborCost: 0,
          partsCost: 0,
          paintCost: 0,
          breakdown: [],
        },
      };
    } catch (error) {
      console.error('Error analyzing image:', error);
      throw new Error('Failed to analyze image');
    }
  }

  static async getAnalysisHistory(userId: string): Promise<DamageAnalysis[]> {
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    return [
      {
        id: '1',
        userId,
        imageUri: 'https://images.pexels.com/photos/1638459/pexels-photo-1638459.jpeg',
        analysisDate: new Date(Date.now() - 86400000), // 1 day ago
        damageDetected: true,
        damageType: [
          {
            type: 'Scratch',
            location: 'Rear bumper',
            severity: 'Minor',
            coordinates: { x: 150, y: 250, width: 100, height: 20 }
          }
        ],
        severity: 'Minor',
        costEstimation: {
          totalCost: 450,
          laborCost: 200,
          partsCost: 150,
          paintCost: 100,
          breakdown: [
            { item: 'Scratch repair', cost: 200, category: 'Labor', description: 'Sand and fill scratch' },
            { item: 'Paint matching', cost: 100, category: 'Paint', description: 'Color match rear bumper' },
            { item: 'Touch-up kit', cost: 150, category: 'Parts', description: 'Professional touch-up materials' }
          ]
        },
        status: 'Completed',
        confidence: 0.92
      },
      {
        id: '2',
        userId,
        imageUri: 'https://images.pexels.com/photos/3764984/pexels-photo-3764984.jpeg',
        analysisDate: new Date(Date.now() - 172800000), // 2 days ago
        damageDetected: false,
        damageType: [],
        severity: 'Minor',
        costEstimation: {
          totalCost: 0,
          laborCost: 0,
          partsCost: 0,
          paintCost: 0,
          breakdown: []
        },
        status: 'Completed',
        confidence: 0.88
      }
    ];
  }
}