'use client'

import React, { useState, useRef } from 'react'
import { Camera, Upload, RefreshCw, Volume2, Check, X } from 'lucide-react'
import axios from 'axios'

interface Ingredient {
  name: string
  confidence: number
  available: boolean
}

interface Recipe {
  title: string
  ingredients: string[]
  instructions: string[]
  cookingTime: string
}

export default function Home() {
  const [image, setImage] = useState<string | null>(null)
  const [ingredients, setIngredients] = useState<Ingredient[]>([])
  const [recipe, setRecipe] = useState<Recipe | null>(null)
  const [loading, setLoading] = useState(false)
  const [processingStep, setProcessingStep] = useState('')
  const fileInputRef = useRef<HTMLInputElement>(null)
  const cameraInputRef = useRef<HTMLInputElement>(null)

  const handleImageUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setImage(e.target?.result as string)
        processImage(file)
      }
      reader.readAsDataURL(file)
    }
  }

  const processImage = async (file: File) => {
    setLoading(true)
    setProcessingStep('Detecting ingredients...')
    
    try {
      const formData = new FormData()
      formData.append('image', file)

      // Detect ingredients
      const ingredientsResponse = await axios.post('/api/backend/detect-ingredients', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const detectedIngredients: Ingredient[] = ingredientsResponse.data.ingredients.map((ing: any) => ({
        ...ing,
        available: true
      }))
      
      setIngredients(detectedIngredients)
      setProcessingStep('Generating recipe...')

      // Generate recipe
      const recipeResponse = await axios.post('/api/backend/generate-recipe', {
        ingredients: detectedIngredients.filter(ing => ing.available).map(ing => ing.name)
      })

      setRecipe(recipeResponse.data.recipe)
    } catch (error) {
      console.error('Error processing image:', error)
      alert('Error processing image. Please try again.')
    } finally {
      setLoading(false)
      setProcessingStep('')
    }
  }

  const regenerateRecipe = async () => {
    if (ingredients.length === 0) return
    
    setLoading(true)
    setProcessingStep('Generating new recipe...')
    
    try {
      const recipeResponse = await axios.post('/api/backend/generate-recipe', {
        ingredients: ingredients.filter(ing => ing.available).map(ing => ing.name),
        regenerate: true
      })
      setRecipe(recipeResponse.data.recipe)
    } catch (error) {
      console.error('Error regenerating recipe:', error)
      alert('Error generating recipe. Please try again.')
    } finally {
      setLoading(false)
      setProcessingStep('')
    }
  }

  const toggleIngredientAvailability = (index: number) => {
    const newIngredients = [...ingredients]
    newIngredients[index].available = !newIngredients[index].available
    setIngredients(newIngredients)
  }

  const speakRecipe = async () => {
    if (!recipe) return
    
    try {
      const text = `Recipe: ${recipe.title}. Ingredients: ${recipe.ingredients.join(', ')}. Instructions: ${recipe.instructions.join('. ')}`
      const response = await axios.post('/api/backend/text-to-speech', { text })
      
      if (response.data.audio_url) {
        const audio = new Audio(response.data.audio_url)
        audio.play()
      }
    } catch (error) {
      console.error('Error with text-to-speech:', error)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-red-50">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold gradient-bg bg-clip-text text-transparent mb-4">
            RecipeSnap
          </h1>
          <p className="text-gray-600 text-lg">
            AI-powered cooking assistant that analyzes your fridge ingredients
          </p>
        </div>

        {/* Image Upload Section */}
        <div className="max-w-2xl mx-auto mb-8">
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4">Upload Your Fridge Photo</h2>
            
            {!image ? (
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                <div className="flex flex-col items-center space-y-4">
                  <div className="flex space-x-4">
                    <button
                      onClick={() => fileInputRef.current?.click()}
                      className="flex items-center space-x-2 bg-primary-500 text-white px-6 py-3 rounded-lg hover:bg-primary-600 transition-colors"
                    >
                      <Upload size={20} />
                      <span>Upload Photo</span>
                    </button>
                    <button
                      onClick={() => cameraInputRef.current?.click()}
                      className="flex items-center space-x-2 bg-gray-500 text-white px-6 py-3 rounded-lg hover:bg-gray-600 transition-colors"
                    >
                      <Camera size={20} />
                      <span>Take Photo</span>
                    </button>
                  </div>
                  <p className="text-gray-500">Upload or capture an image of your fridge ingredients</p>
                </div>
              </div>
            ) : (
              <div className="space-y-4">
                <img
                  src={image}
                  alt="Uploaded ingredients"
                  className="w-full h-64 object-cover rounded-lg"
                />
                <button
                  onClick={() => {
                    setImage(null)
                    setIngredients([])
                    setRecipe(null)
                  }}
                  className="text-gray-500 hover:text-gray-700"
                >
                  Upload different image
                </button>
              </div>
            )}

            <input
              ref={fileInputRef}
              type="file"
              accept="image/*"
              onChange={handleImageUpload}
              className="hidden"
            />
            <input
              ref={cameraInputRef}
              type="file"
              accept="image/*"
              capture="environment"
              onChange={handleImageUpload}
              className="hidden"
            />
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-white rounded-lg shadow-lg p-6 text-center">
              <div className="animate-spin w-8 h-8 border-4 border-primary-500 border-t-transparent rounded-full mx-auto mb-4"></div>
              <p className="text-gray-600">{processingStep}</p>
            </div>
          </div>
        )}

        {/* Detected Ingredients */}
        {ingredients.length > 0 && (
          <div className="max-w-2xl mx-auto mb-8">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h2 className="text-2xl font-semibold mb-4">Detected Ingredients</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                {ingredients.map((ingredient, index) => (
                  <div
                    key={index}
                    className={`flex items-center space-x-2 p-3 rounded-lg border cursor-pointer transition-colors ${
                      ingredient.available
                        ? 'border-green-200 bg-green-50'
                        : 'border-gray-200 bg-gray-50'
                    }`}
                    onClick={() => toggleIngredientAvailability(index)}
                  >
                    {ingredient.available ? (
                      <Check size={16} className="text-green-600" />
                    ) : (
                      <X size={16} className="text-gray-400" />
                    )}
                    <span className={ingredient.available ? 'text-green-800' : 'text-gray-500'}>
                      {ingredient.name}
                    </span>
                    <span className="text-xs text-gray-400">
                      {Math.round(ingredient.confidence * 100)}%
                    </span>
                  </div>
                ))}
              </div>
              <p className="text-sm text-gray-500 mt-4">
                Click ingredients to mark them as available/unavailable
              </p>
            </div>
          </div>
        )}

        {/* Recipe */}
        {recipe && (
          <div className="max-w-2xl mx-auto">
            <div className="bg-white rounded-lg shadow-lg p-6">
              <div className="flex justify-between items-start mb-4">
                <h2 className="text-2xl font-semibold">{recipe.title}</h2>
                <div className="flex space-x-2">
                  <button
                    onClick={speakRecipe}
                    className="p-2 text-gray-600 hover:text-primary-600 transition-colors"
                    title="Listen to recipe"
                  >
                    <Volume2 size={20} />
                  </button>
                  <button
                    onClick={regenerateRecipe}
                    className="flex items-center space-x-2 text-primary-600 hover:text-primary-700 transition-colors"
                    disabled={loading}
                  >
                    <RefreshCw size={16} className={loading ? 'animate-spin' : ''} />
                    <span>Regenerate</span>
                  </button>
                </div>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold mb-2">Cooking Time</h3>
                  <p className="text-gray-600">{recipe.cookingTime}</p>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">Ingredients</h3>
                  <ul className="list-disc list-inside space-y-1">
                    {recipe.ingredients.map((ingredient, index) => (
                      <li key={index} className="text-gray-600">{ingredient}</li>
                    ))}
                  </ul>
                </div>

                <div>
                  <h3 className="font-semibold mb-2">Instructions</h3>
                  <ol className="list-decimal list-inside space-y-2">
                    {recipe.instructions.map((instruction, index) => (
                      <li key={index} className="text-gray-600">{instruction}</li>
                    ))}
                  </ol>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500">
          <p>Powered by AI • All models run locally</p>
        </div>
      </div>
    </div>
  )
} 